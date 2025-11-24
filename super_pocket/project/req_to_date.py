import httpx, re, asyncio, uvicorn, click
import tomllib
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
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PackageInput(BaseModel):
    package: str
    version: str


class PackageResult(BaseModel):
    package: str
    current_version: str
    latest_patch: Optional[str] = None
    latest_overall: Optional[str] = None
    status: str
    message: Optional[str] = None


class CheckRequest(BaseModel):
    packages: List[PackageInput]


def _read_requirements_file(path: Path) -> List[str]:
    """Retourne les dépendances extraites d'un fichier requirements."""
    try:
        with open(path, "r") as f:
            lines = [l.strip() for l in f.readlines()[2:]]

    except FileNotFoundError as exc:
        raise exc(f"Fichier requirements introuvable: {path}: {exc}")
    except OSError as exc:
        raise exc(f"Impossible de lire {path}: {exc}")

    specs: List[str] = []
    for line in lines:
        if not line or line.startswith("#") or line.startswith("--"):
            continue
        else:
            specs.append(line)

    if not specs:
        raise ValueError(f"Aucun package valide trouvé dans {path}")

    return specs


def _read_pyproject_file(path: Path) -> List[str]:
    """Retourne les dépendances extraites d'un fichier pyproject.toml."""
    try:
        content = path.read_bytes()
    except FileNotFoundError:
        raise ValueError(f"Fichier pyproject.toml introuvable: {path}") from None
    except OSError as exc:
        raise ValueError(f"Impossible de lire {path}: {exc}") from None

    try:
        data = tomllib.loads(content.decode("utf-8"))
    except tomllib.TOMLDecodeError as exc:
        raise ValueError(f"Erreur de parsing TOML dans {path}: {exc}") from None

    specs: List[str] = []
    
    # Extraire les dépendances principales
    dependencies = data.get("project", {}).get("dependencies", [])
    for dep in dependencies:
        # Convertir les spécificateurs de version en format ==version
        # Supporte: package>=1.0.0, package~=1.0, package==1.0.0, etc.
        spec = _normalize_dependency_spec(dep)
        if spec:
            specs.append(spec)
    
    # Optionnel: extraire aussi les dépendances optionnelles
    optional_deps = data.get("project", {}).get("optional-dependencies", {})
    for group_name, group_deps in optional_deps.items():
        for dep in group_deps:
            spec = _normalize_dependency_spec(dep)
            if spec:
                specs.append(spec)

    if not specs:
        raise ValueError(f"Aucune dépendance trouvée dans {path}")

    return specs


def _normalize_dependency_spec(dep: str) -> Optional[str]:
    """Normalise une spécification de dépendance en format package==version."""
    # Si déjà au format package==version, retourner tel quel
    if "==" in dep:
        return dep
    
    # Extraire le nom du package et la version pour les autres formats
    # Supporte: >=, ~=, >, <, <=, !=
    match = re.match(r'^([a-zA-Z0-9_-]+)\s*([><=!~]+)\s*(.+)$', dep)
    if match:
        package = match.group(1)
        operator = match.group(2)
        version = match.group(3)
        
        # Pour >=, ~=, utiliser la version minimale spécifiée
        if operator in (">=", "~=", ">"):
            return f"{package}=={version}"

        # Pour ==, retourner tel quel
        elif operator == "==":
            return dep
    
    # Si pas de version spécifiée, ignorer
    return None


def _expand_spec_inputs(inputs: Sequence[str]) -> List[str]:
    """Décompose les arguments CLI: virgules, fichiers requirements, pyproject.toml, etc."""
    expanded: List[str] = []
    for entry in inputs:
        if not entry:
            continue
        entry = entry.strip()

        # Gestion des listes séparées par des virgules dans un seul argument
        if ',' in entry:
            parts = [part.strip() for part in entry.split(',')]
            expanded.extend(parts)
            continue

        potential_path = Path(entry).expanduser()
        if potential_path.is_file():
            # Détecter le type de fichier et utiliser le parser approprié
            if potential_path.name == "pyproject.toml":
                expanded.extend(_read_pyproject_file(potential_path))
            else:
                # Par défaut, traiter comme un fichier requirements.txt
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
                    current_version=version,
                    status="error",
                    message=f"Paquet introuvable (code {response.status_code})"
                )
            
            data = response.json()
            all_versions = list(data.get('releases', {}).keys())
            latest_patch = find_latest_patch(version, all_versions)
            
            return PackageResult(
                package=pkg,
                current_version=version,
                latest_patch=latest_patch,
                latest_overall=data['info']['version'],
                status='outdated' if latest_patch else 'up-to-date'
            )
            
        except httpx.TimeoutException:
            return PackageResult(
                package=pkg,
                current_version=version,
                status="error",
                message="Timeout lors de la requête à PyPI"
            )
        except Exception as e:
            return PackageResult(
                package=pkg,
                current_version=version,
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
    packages = _expand_spec_inputs(packages)
    count = 0
    try:
        results = run_req_to_date(packages)
    except ValueError as exc:
        raise click.BadParameter(str(exc))

    for result in results:
        if result.current_version != result.latest_overall:
            click.echo(
                f"\033[31m{result.package} {result.current_version})\033[0m ---> "
                f"\033[32m {result.latest_overall}\033[0m"
            )
            count += 1
    if count == 0:
        click.echo("Aucune mise à jour disponible")
