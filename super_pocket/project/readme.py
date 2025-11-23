"""Interactive README generator for software projects.

This module scans a target project directory to infer its technology stack
(languages, frameworks, dependencies) and a probable project type
(e.g., CLI tool, web application, REST API). It then runs a small
interactive wizard to help the user generate a high-quality README.md.

All public functions are designed to be called from the Pocket CLI.
"""

from __future__ import annotations

import json, os, tomllib, click
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from .to_file import LANG_MAP


# ==================== Data Models ====================

@dataclass
class ProjectInfo:
    """Summary of a scanned project.

    This structure is intentionally simple and focused on what is
    most useful for generating a good README.
    """

    root: Path
    main_language: Optional[str]
    other_languages: List[str] = field(default_factory=list)
    dependencies: Dict[str, List[str]] = field(default_factory=dict)
    frameworks: List[str] = field(default_factory=list)
    project_type: Optional[str] = None


@dataclass
class ReadmeUserChoices:
    """User-provided customization options for README generation."""

    project_name: str
    short_description: str
    long_description: str
    include_install: bool
    install_commands: List[str]
    include_usage: bool
    usage_examples: List[str]
    include_contributing: bool
    include_license: bool


# ==================== High-level API ====================

def run_readme_wizard(project_path: str, output: Optional[str] = None) -> None:
    """Scan a project and guide the user through README generation.

    Args:
        project_path: File system path to the project root directory.
        output: Optional explicit README file path. If omitted, defaults to
            README.md inside the project root.
    """

    root = Path(project_path).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise click.BadParameter(f"Project path does not exist or is not a directory: {root}")

    click.echo(f"Scanning project at: {root}")
    info = scan_project(root)

    click.echo("\nDetected project profile:")
    click.echo(f"  - Main language: {info.main_language or 'unknown'}")
    if info.other_languages:
        click.echo(f"  - Other languages: {', '.join(info.other_languages)}")
    if info.frameworks:
        click.echo(f"  - Frameworks: {', '.join(info.frameworks)}")
    if info.dependencies:
        eco_summaries = [
            f"{eco}: {', '.join(deps[:5])}{'…' if len(deps) > 5 else ''}"
            for eco, deps in info.dependencies.items()
        ]
        click.echo(f"  - Dependencies: {', '.join(eco_summaries)}")
    if info.project_type:
        click.echo(f"  - Inferred project type: {info.project_type}")

    choices = ask_user_for_readme_preferences(info)

    content = build_readme_content(info, choices)

    if output is None:
        output_path = root / "README.md"
    else:
        output_path = Path(output).expanduser().resolve()

    if output_path.exists():
        overwrite = click.confirm(
            f"README file already exists at {output_path}. Do you want to overwrite it?",
            default=False,
        )
        if not overwrite:
            click.echo("Aborting without writing README.")
            return

    output_path.write_text(content, encoding="utf-8")
    click.echo(f"\nREADME generated at: {output_path}")


# ==================== Scanning Logic ====================

PYTHON_DEP_FILES = ["pyproject.toml", "requirements.txt"]
NODE_DEP_FILES = ["package.json"]


def scan_project(root: Path) -> ProjectInfo:
    """Inspect the project folder and extract high-level characteristics."""

    languages = detect_languages(root)
    dependencies = detect_dependencies(root)
    frameworks, project_type = detect_frameworks_and_type(languages, dependencies, root)

    main_language = None
    other_languages: List[str] = []
    if languages:
        sorted_langs = sorted(languages.items(), key=lambda item: item[1], reverse=True)
        main_language = sorted_langs[0][0]
        other_languages = [name for name, _count in sorted_langs[1:]]

    return ProjectInfo(
        root=root,
        main_language=main_language,
        other_languages=other_languages,
        dependencies=dependencies,
        frameworks=frameworks,
        project_type=project_type,
    )


def detect_languages(root: Path) -> Dict[str, int]:
    """Count languages by file extension using the existing LANG_MAP.

    Returns a mapping "language name" -> count of files.
    """

    ext_to_lang = {ext: lang for ext, lang in LANG_MAP.items() if ext.startswith(".")}
    counts: Dict[str, int] = {}

    for dirpath, dirnames, filenames in os.walk(root):
        # Basic pruning of common non-source directories
        dirnames[:] = [
            d
            for d in dirnames
            if d not in {"docs", "tests", "_build", "dist", "build", "_static", ".cursor", ".codex", ".claude", ".git", "node_modules", "dist", "build", "__pycache__", ".venv", "venv"}
        ]

        for name in filenames:
            _, ext = os.path.splitext(name)
            lang = ext_to_lang.get(ext.lower())
            if not lang:
                continue
            counts[lang] = counts.get(lang, 0) + 1

    return counts


def detect_dependencies(root: Path) -> Dict[str, List[str]]:
    """Detect dependencies from common manifest files.

    Currently supports Python (pyproject, requirements.txt) and Node (package.json).
    """

    deps: Dict[str, List[str]] = {"python": [], "node": []}

    for filename in PYTHON_DEP_FILES:
        path = root / filename
        if path.is_file():
            deps["python"].extend(parse_python_deps(path))

    package_json = root / "package.json"
    if package_json.is_file():
        deps["node"].extend(parse_node_deps(package_json))

    # Remove empty ecosystems
    return {eco: sorted(set(names)) for eco, names in deps.items() if names}


def parse_python_deps(path: Path) -> List[str]:
    """Parse a Python dependency file into a list of package names."""

    if path.name == "requirements.txt":
        names: List[str] = []
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # Remove version specifiers and extras very roughly
            for sep in ["==", ">=", "<=", "~=", "!=" , ">", "<"]:
                if sep in line:
                    line = line.split(sep, 1)[0]
                    break
            if "[" in line:
                line = line.split("[", 1)[0]
            if line:
                names.append(line)
        return names

    if path.name == "pyproject.toml":
        try:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
            deps: List[str] = []
            # PEP 621 style
            proj = data.get("project") or {}
            for item in proj.get("dependencies", []) or []:
                if isinstance(item, str):
                    name = item.split(" ", 1)[0]
                    name = name.split("[", 1)[0]
                    deps.append(name)
            # Optional tool-specific sections can be added here later
            return deps
        except Exception:
            # Fallback to a very naive line-based parse
            return []

    return []


def parse_node_deps(path: Path) -> List[str]:
    """Parse Node dependencies from package.json."""

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return []

    names: Set[str] = set()
    for key in ("dependencies", "devDependencies", "peerDependencies"):
        section = data.get(key) or {}
        if isinstance(section, dict):
            names.update(section.keys())
    return sorted(names)


def detect_frameworks_and_type(
    languages: Dict[str, int],
    dependencies: Dict[str, List[str]],
    root: Path,
) -> Tuple[List[str], Optional[str]]:
    """Infer frameworks and a probable project type from the scan results."""

    frameworks: Set[str] = set()
    project_type: Optional[str] = None

    python_deps = {name.lower() for name in dependencies.get("python", [])}
    node_deps = {name.lower() for name in dependencies.get("node", [])}

    # Python web frameworks
    if "django" in python_deps:
        frameworks.add("Django")
    if "flask" in python_deps:
        frameworks.add("Flask")
    if "fastapi" in python_deps:
        frameworks.add("FastAPI")
    if "starlette" in python_deps:
        frameworks.add("Starlette")

    # Python CLI helpers
    if "click" in python_deps:
        frameworks.add("Click")
    if "typer" in python_deps:
        frameworks.add("Typer")

    # Node / frontend frameworks
    if "react" in node_deps:
        frameworks.add("React")
    if "next" in node_deps or "next.js" in node_deps:
        frameworks.add("Next.js")
    if "vue" in node_deps:
        frameworks.add("Vue.js")
    if "nuxt" in node_deps:
        frameworks.add("Nuxt.js")
    if "angular" in node_deps or "@angular/core" in node_deps:
        frameworks.add("Angular")
    if "express" in node_deps:
        frameworks.add("Express")
    if "nestjs" in node_deps:
        frameworks.add("NestJS")

    # Guess project type based on signals
    main_lang = None
    if languages:
        main_lang = max(languages.items(), key=lambda item: item[1])[0]

    if main_lang == "python":
        if {"fastapi", "flask", "django"} and python_deps:
            project_type = "Web application / REST API (Python)"
        elif {"click", "typer"} and python_deps:
            project_type = "Command-line tool (Python)"
        else:
            project_type = "Python library or application"

    elif main_lang in {"javascript", "typescript"}:
        if {"react", "next", "vue", "angular", "nuxt"} & node_deps:
            project_type = "Web application (JavaScript / TypeScript)"
        elif {"express", "nestjs"} & node_deps:
            project_type = "Web API / backend service (Node.js)"
        else:
            project_type = "JavaScript / TypeScript application"

    # Look for simple heuristics in the tree (e.g., presence of Dockerfile)
    if not project_type:
        if (root / "Dockerfile").is_file():
            project_type = "Containerized service"

    return sorted(frameworks), project_type


# ==================== Interactive Wizard ====================

def ask_user_for_readme_preferences(info: ProjectInfo) -> ReadmeUserChoices:
    """Ask the user a few questions to customize the README content."""

    default_name = info.root.name
    project_name = click.prompt(
        "Project name",
        default=default_name,
    )

    short_description = click.prompt(
        "Short one-line description",
        default=f"{info.project_type or 'Software project'} built with {info.main_language or 'multiple languages'}",
    )

    long_description = click.prompt(
        "Longer description (you can refine later)",
        default="",
        show_default=False,
    )

    include_install = click.confirm("Include installation section ?", default=True)
    install_commands: List[str] = []
    if include_install:
        suggested_cmds = suggest_install_commands(info)
        if suggested_cmds:
            click.echo("Suggested installation commands:")
            for cmd in suggested_cmds:
                click.echo(f"  - {cmd}")
        install_block = click.prompt(
            "Installation commands (multi-line, separated by ';', leave empty to use suggestions only)",
            default="",
            show_default=False,
        )
        if install_block.strip():
            install_commands.extend([c.strip() for c in install_block.split(";") if c.strip()])
        else:
            install_commands.extend(suggested_cmds)

    include_usage = click.confirm("Include usage section ?", default=True)
    usage_examples: List[str] = []
    if include_usage:
        usage_block = click.prompt(
            "Usage examples (multi-line, separated by ';', you can leave empty)",
            default="",
            show_default=False,
        )
        if usage_block.strip():
            usage_examples.extend([u.strip() for u in usage_block.split(";") if u.strip()])

    include_contributing = click.confirm("Include contributing section?", default=True)
    include_license = click.confirm("Include license section?", default=True)

    return ReadmeUserChoices(
        project_name=project_name,
        short_description=short_description,
        long_description=long_description,
        include_install=include_install,
        install_commands=install_commands,
        include_usage=include_usage,
        usage_examples=usage_examples,
        include_contributing=include_contributing,
        include_license=include_license,
    )


def suggest_install_commands(info: ProjectInfo) -> List[str]:
    """Provide a small list of best-effort installation commands."""

    cmds: List[str] = []

    if info.main_language == "python":
        if (info.root / "requirements.txt").is_file():
            cmds.append("pip install -r requirements.txt")
        elif (info.root / "pyproject.toml").is_file():
            cmds.append("pip install .")

    if info.main_language in {"javascript", "typescript"}:
        if (info.root / "package-lock.json").is_file() or (info.root / "npm-shrinkwrap.json").is_file():
            cmds.append("npm install")
        elif (info.root / "yarn.lock").is_file():
            cmds.append("yarn install")
        elif (info.root / "pnpm-lock.yaml").is_file():
            cmds.append("pnpm install")
        else:
            if (info.root / "package.json").is_file():
                cmds.append("npm install")

    if not cmds:
        cmds.append("<add your installation steps here>")

    return cmds


# ==================== README Content Rendering ====================

def build_readme_content(info: ProjectInfo, choices: ReadmeUserChoices) -> str:
    """Render the final README Markdown content."""

    lines: List[str] = []

    # Title and short description
    lines.append(f"# {choices.project_name}")
    lines.append("")
    lines.append(choices.short_description)
    lines.append("")

    if choices.long_description.strip():
        lines.append(choices.long_description.strip())
        lines.append("")

    # Tech stack section
    tech_stack_lines: List[str] = []
    if info.main_language:
        tech_stack_lines.append(f"- **Main language**: {info.main_language}")
    if info.other_languages:
        tech_stack_lines.append(f"- **Other languages**: {', '.join(info.other_languages)}")
    if info.frameworks:
        tech_stack_lines.append(f"- **Frameworks / libraries**: {', '.join(info.frameworks)}")
    if info.dependencies:
        eco_parts = []
        for eco, deps in info.dependencies.items():
            sample = ", ".join(deps[:5])
            suffix = "…" if len(deps) > 5 else ""
            eco_parts.append(f"{eco}: {sample}{suffix}")
        tech_stack_lines.append(f"- **Dependencies**: {', '.join(eco_parts)}")
    if info.project_type:
        tech_stack_lines.append(f"- **Project type**: {info.project_type}")

    if tech_stack_lines:
        lines.append("## Tech stack")
        lines.append("")
        lines.extend(tech_stack_lines)
        lines.append("")

    # Installation
    if choices.include_install and choices.install_commands:
        lines.append("## Installation")
        lines.append("")
        lines.append("Run the following commands to set up the project:")
        lines.append("")
        lines.append("```bash")
        for cmd in choices.install_commands:
            lines.append(cmd)
        lines.append("```")
        lines.append("")

    # Usage
    if choices.include_usage:
        lines.append("## Usage")
        lines.append("")
        if choices.usage_examples:
            for ex in choices.usage_examples:
                lines.append("```bash")
                lines.append(ex)
                lines.append("```")
                lines.append("")
        else:
            lines.append("Describe how to run and use this project here.")
            lines.append("")

    # Contributing
    if choices.include_contributing:
        lines.append("## Contributing")
        lines.append("")
        lines.append("Contributions, issues and feature requests are welcome.")
        lines.append("Feel free to open an issue or submit a pull request.")
        lines.append("")

    # License
    if choices.include_license:
        lines.append("## License")
        lines.append("")
        lines.append("This project is licensed. Add the license name and details here (e.g., MIT, Apache-2.0).")
        lines.append("")

    return "\n".join(lines)
