import httpx, re, asyncio, uvicorn, click
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Sequence


app = FastAPI(title="Requirements Checker API")

# Configuration CORS pour permettre les requêtes du frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifie les origines autorisées
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PackageInput(BaseModel):
    package: str
    version: str


class PackageResult(BaseModel):
    package: str
    currentVersion: str
    latestPatch: Optional[str] = None
    latestOverall: Optional[str] = None
    status: str
    message: Optional[str] = None


class CheckRequest(BaseModel):
    packages: List[PackageInput]


def _read_requirements_file(path: Path) -> List[str]:
    """Retourne les dépendances extraites d'un fichier requirements."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        raise ValueError(f"Fichier requirements introuvable: {path}") from None
    except OSError as exc:
        raise ValueError(f"Impossible de lire {path}: {exc}") from None

    specs: List[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("-r") or line.startswith("--"):
            raise ValueError(
                f"Les références imbriquées ou options pip ne sont pas supportées: '{line}'"
            )
        specs.append(line)

    if not specs:
        raise ValueError(f"Aucun package valide trouvé dans {path}")

    return specs


def _expand_spec_inputs(inputs: Sequence[str]) -> List[str]:
    """Décompose les arguments CLI: virgules, fichiers requirements, etc."""
    expanded: List[str] = []
    for entry in inputs:
        if entry is None:
            continue
        entry = entry.strip()
        if not entry:
            continue

        # Gestion des listes séparées par des virgules dans un seul argument
        if ',' in entry and not Path(entry).exists():
            parts = [part.strip() for part in entry.split(',') if part.strip()]
            expanded.extend(parts)
            continue

        potential_path = Path(entry).expanduser()
        if potential_path.is_file():
            expanded.extend(_read_requirements_file(potential_path))
            continue

        expanded.append(entry)

    if not expanded:
        raise ValueError("La liste de packages ne peut pas être vide")

    return expanded


def parse_package_specs(specs: Sequence[str]) -> List[PackageInput]:
    """Convertit la liste d'arguments CLI en objets PackageInput."""
    expanded_specs = _expand_spec_inputs(specs)
    parsed: List[PackageInput] = []
    for spec in expanded_specs:
        if "==" not in spec:
            raise ValueError("Chaque package doit être fourni sous la forme nom==version")
        package, version = spec.split("==", 1)
        package = package.strip()
        version = version.strip()
        if not package or not version:
            raise ValueError(f"Format invalide pour '{spec}': nom ou version manquant")
        parsed.append(PackageInput(package=package, version=version))

    return parsed


def parse_version(version_str: str) -> Optional[dict]:
    """Parse une version en format semver"""
    match = re.match(r'^(\d+)\.(\d+)\.(\d+)', version_str)
    if not match:
        return None
    return {
        'major': int(match.group(1)),
        'minor': int(match.group(2)),
        'patch': int(match.group(3)),
        'full': version_str
    }


def find_latest_patch(current_version: str, all_versions: List[str]) -> Optional[str]:
    """Trouve la dernière version patch compatible"""
    current = parse_version(current_version)
    if not current:
        return None
    
    compatible_versions = []
    for v in all_versions:
        parsed = parse_version(v)
        if (parsed and 
            parsed['major'] == current['major'] and 
            parsed['minor'] == current['minor'] and 
            parsed['patch'] > current['patch']):
            compatible_versions.append(parsed)
    
    if not compatible_versions:
        return None
    
    # Trier par patch décroissant et retourner le premier
    compatible_versions.sort(key=lambda x: x['patch'], reverse=True)
    return compatible_versions[0]['full']


async def check_package(pkg: str, version: str) -> PackageResult:
    """Vérifie un package sur PyPI"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"https://pypi.org/pypi/{pkg}/json",
                timeout=10.0
            )
            
            if response.status_code != 200:
                return PackageResult(
                    package=pkg,
                    currentVersion=version,
                    status="error",
                    message=f"Paquet introuvable (code {response.status_code})"
                )
            
            data = response.json()
            all_versions = list(data.get('releases', {}).keys())
            latest_patch = find_latest_patch(version, all_versions)
            
            return PackageResult(
                package=pkg,
                currentVersion=version,
                latestPatch=latest_patch,
                latestOverall=data['info']['version'],
                status='outdated' if latest_patch else 'up-to-date'
            )
            
        except httpx.TimeoutException:
            return PackageResult(
                package=pkg,
                currentVersion=version,
                status="error",
                message="Timeout lors de la requête à PyPI"
            )
        except Exception as e:
            return PackageResult(
                package=pkg,
                currentVersion=version,
                status="error",
                message=str(e)
            )


@app.get("/")
async def root():
    return {
        "message": "Requirements Checker API",
        "endpoints": {
            "/check": "POST - Vérifie les dépendances",
            "/docs": "Documentation interactive"
        }
    }


async def _check_packages(request_packages: List[PackageInput]) -> List[PackageResult]:
    """Lance les vérifications sur PyPI pour la liste fournie."""
    tasks = [check_package(pkg.package.lower(), pkg.version) for pkg in request_packages]
    return await asyncio.gather(*tasks)


@app.post("/check", response_model=List[PackageResult])
async def check_packages(request: CheckRequest):
    """
    Vérifie une liste de packages et retourne les mises à jour disponibles
    """
    if not request.packages:
        raise HTTPException(status_code=400, detail="Liste de packages vide")

    return await _check_packages(request.packages)


async def check_packages_from_specs(specs: Sequence[str]) -> List[PackageResult]:
    """Interface utilitaire pour la ligne de commande."""
    packages = parse_package_specs(specs)
    return await _check_packages(packages)


def run_req_to_date(packages: Sequence[str]) -> List[PackageResult]:
    """Point d'entrée synchrone pour les CLI (standalone ou via pocket)."""
    return asyncio.run(check_packages_from_specs(packages))


@click.command(name="req-to-date")
@click.argument("packages", nargs=-1)
def req_to_date_cli(packages: tuple[str, ...]):
    """Commande standalone: accepte nom==version, liste avec virgules ou requirements.txt."""
    if not packages:
        raise click.BadParameter(
            "Fournissez au moins un package, une liste séparée par des virgules ou un fichier requirements.txt.",
            ctx=click.get_current_context(),
            param_hint="packages"
        )

    try:
        results = run_req_to_date(packages)
    except ValueError as exc:
        raise click.BadParameter(str(exc))

    for result in results:
        if not result.currentVersion == result.latestOverall:
            click.echo(
                f"{result.package} (installée: {result.currentVersion}) -> "
                f"patch: {result.latestPatch or '-'} | dernière: {result.latestOverall} | statut: {result.status}"
            )
