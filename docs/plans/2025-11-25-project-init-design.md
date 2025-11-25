# Project Initialization Tool Design

**Date**: 2025-11-25
**Feature**: `pocket project init` - Hybrid template-based project scaffolding tool

## Overview

A comprehensive project initialization tool that combines speed (templates) with flexibility (interactive customization). Users select a base template, then interactively customize tool choices and toggle features. The tool generates complete project structures with sensible defaults for Python development across multiple domains.

## Problem Statement

Starting new Python projects involves repetitive manual setup:
- Creating virtual environments and managing dependencies
- Writing boilerplate pyproject.toml/requirements files
- Setting up folder structures (src/, tests/, docs/)
- Configuring development tools (pytest, ruff, black, pre-commit)
- Domain-specific setup (ML directories, API scaffolding, CLI entry points)

This tool automates the full project initialization workflow with smart defaults and customization options.

## Architecture

### Approach: Declarative Templates with Python Engine

**Core Concept**: Use YAML manifests to define templates (structure, options, files) with Python handling rendering and execution.

**Benefits**:
- Easy template creation/modification (non-programmers can contribute)
- Clear separation: template definitions (data) vs execution logic (code)
- Self-contained templates, easy to version and test
- Python available for complex logic when needed

**Alternatives Considered**:
- Template-as-Code: Too rigid, hard for non-coders to contribute
- Directory Templates (cookiecutter-style): Doesn't scale well to 6+ templates, file-based conditionals messy

## CLI Interface

### Commands

```bash
# List available templates
pocket project init --list

# Preview template details
pocket project init --show python-cli

# Initialize with interactive customization
pocket project init python-cli

# Quick init with all defaults
pocket project init python-cli --quick

# Initialize in specific directory
pocket project init python-cli --path ./my-project
```

### User Flow

1. User runs `pocket project init <template-name>`
2. Tool loads template manifest from `super_pocket/project/templates/<template-name>.yaml`
3. Presents interactive customization UI (tool choices + feature toggles)
4. User makes selections via beautiful TUI
5. Tool generates project structure based on selections
6. Writes files, creates venv, installs dependencies
7. Displays summary with next steps

## Module Structure

```
super_pocket/project/
├── init/
│   ├── __init__.py
│   ├── cli.py              # Click commands for init subcommands
│   ├── engine.py           # Core project generation logic
│   ├── manifest.py         # Template manifest parser/validator
│   ├── interactive.py      # TUI for customization using rich/questionary
│   └── renderers.py        # Jinja2 file rendering
└── templates/
    ├── python-cli.yaml
    ├── python-cli/         # Template files for CLI projects
    │   ├── init.py.j2
    │   ├── cli_click.py.j2
    │   ├── cli_typer.py.j2
    │   ├── pyproject_uv.toml.j2
    │   └── ...
    ├── fastapi-api.yaml
    ├── fastapi-api/        # Template files for API projects
    ├── python-package.yaml
    ├── python-package/
    ├── ml-project.yaml
    ├── ml-project/
    ├── automation-script.yaml
    ├── automation-script/
    ├── docs-site.yaml
    └── docs-site/
```

## Template Manifest Format

### YAML Schema

Each template is defined in a YAML file:

```yaml
# python-cli.yaml
name: python-cli
display_name: "Python CLI Tool"
description: "Command-line tool with Click, rich output, and testing"

python_version: ">=3.11"

# Tool alternatives - user picks one per category
tool_choices:
  cli_framework:
    prompt: "Which CLI framework?"
    default: click
    options:
      - name: click
        description: "Click - composable command line interface"
      - name: typer
        description: "Typer - type hints for CLI (FastAPI style)"
      - name: argparse
        description: "argparse - Standard library (minimal deps)"

  package_manager:
    prompt: "Which package manager?"
    default: uv
    options:
      - name: uv
        description: "uv - blazingly fast (recommended)"
      - name: poetry
        description: "poetry - mature, feature-rich"
      - name: pip
        description: "pip + requirements.txt - simple, universal"

# Feature toggles - user enables/disables each
features:
  - name: rich_output
    description: "Rich terminal output (colors, tables, progress)"
    default: true

  - name: config_file
    description: "Config file support (TOML/YAML parsing)"
    default: false

  - name: testing
    description: "Testing setup with pytest"
    default: true

  - name: github_actions
    description: "GitHub Actions CI/CD workflow"
    default: false

# Directory structure - conditional based on choices
structure:
  - path: "src/{{ project_name }}"
    type: directory

  - path: "src/{{ project_name }}/__init__.py"
    template: "python-cli/init.py.j2"

  - path: "src/{{ project_name }}/cli.py"
    template: "python-cli/cli_{{ tool_choices.cli_framework }}.py.j2"

  - path: "tests/"
    type: directory
    condition: "features.testing"

  - path: "tests/test_cli.py"
    template: "python-cli/test_cli.py.j2"
    condition: "features.testing"

  - path: "pyproject.toml"
    template: "python-cli/pyproject_{{ tool_choices.package_manager }}.toml.j2"

  - path: ".github/workflows/ci.yml"
    template: "python-cli/github_workflow.yaml.j2"
    condition: "features.github_actions"

# Post-generation actions
post_generation:
  - action: git_init

  - action: create_venv
    python_version: "{{ python_version }}"

  - action: install_dependencies
    package_manager: "{{ tool_choices.package_manager }}"
    dev: true

  - action: display_next_steps
```

### Manifest Components

**Metadata**: name, display_name, description, python_version

**tool_choices**: Categories where user picks one option (CLI framework, package manager, database, etc.)

**features**: Boolean toggles for optional components (testing, Docker, CI/CD, etc.)

**structure**: List of files/directories to generate with conditional logic

**post_generation**: Automated setup steps after file generation

## Interactive Customization UI

### User Experience

Rich terminal interface using `rich` library:

```
╭─ Python CLI Tool ────────────────────────────────────────╮
│ Command-line tool with Click, rich output, and testing  │
╰──────────────────────────────────────────────────────────╯

Project name: my-awesome-cli
Description: A CLI tool for awesome things

━━━ Tool Choices ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❯ CLI framework
  ● click - Click - composable command line interface
  ○ typer - Typer - type hints for CLI (FastAPI style)
  ○ argparse - argparse - Standard library (minimal deps)

❯ Package manager
  ● uv - uv - blazingly fast (recommended)
  ○ poetry - poetry - mature, feature-rich
  ○ pip - pip + requirements.txt - simple, universal

━━━ Features ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ☑ Rich terminal output (colors, tables, progress)
  ☐ Config file support (TOML/YAML parsing)
  ☑ Testing setup with pytest
  ☐ GitHub Actions CI/CD workflow

[Enter] Continue  [↑↓] Navigate  [Space] Toggle
```

### Implementation

- Use `rich.prompt` and `questionary` for interactive prompts
- Radio buttons for tool_choices (pick one)
- Checkboxes for features (toggle multiple)
- Text input for project name/description
- Validation ensures compatible selections
- `--quick` flag skips interactive UI, uses all defaults

## Template Rendering

### Jinja2 Context Variables

Templates have access to:
- `project_name` - Project name (snake_case)
- `project_display_name` - Display name (Title Case)
- `description` - Project description
- `tool_choices` - Dict of selected tools
- `features` - Dict of enabled features
- `python_version` - Selected Python version
- Helper functions for transformations

### Example Template (cli_click.py.j2)

```python
import click
{% if features.rich_output %}
from rich.console import Console

console = Console()
{% endif %}

@click.group()
def cli():
    """{{ description }}"""
    pass

@cli.command()
def hello():
    """Say hello"""
    {% if features.rich_output %}
    console.print("[bold green]Hello from {{ project_display_name }}![/bold green]")
    {% else %}
    click.echo("Hello from {{ project_display_name }}!")
    {% endif %}

if __name__ == "__main__":
    cli()
```

### Rendering Process

1. Load manifest and user selections
2. Build Jinja2 context from selections
3. Iterate through `structure` in manifest
4. For each item, evaluate `condition` (if present)
5. Render template with context, write to target path
6. Execute post-generation actions

## Post-Generation Actions

### Automated Setup

After generating files, tool executes setup steps:

```yaml
post_generation:
  - action: git_init
    condition: "features.git"

  - action: create_venv
    python_version: "{{ python_version }}"

  - action: install_dependencies
    package_manager: "{{ tool_choices.package_manager }}"
    dev: true

  - action: run_command
    command: "pre-commit install"
    condition: "features.precommit"

  - action: display_next_steps
```

### Action Types

- **git_init**: Initialize git repo, initial commit
- **create_venv**: Create virtual environment (detects package manager)
- **install_dependencies**: Install packages (runs `uv sync`, `poetry install`, or `pip install`)
- **run_command**: Execute arbitrary shell commands
- **display_next_steps**: Show template-specific instructions

### User Feedback

Rich progress indicators:

```
✓ Generated 12 files
✓ Initialized git repository
⠋ Creating virtual environment...
⠋ Installing dependencies...
```

### Error Handling

Clear error messages with recovery instructions:

```
✗ Failed to create venv: 'uv' command not found

  Install uv with: curl -LsSf https://astral.sh/uv/install.sh | sh
  Or run manually: cd my-project && python -m venv .venv
```

All post-generation actions are optional and skippable.

## The Six Templates

### 1. python-cli (CLI Tools)

**Purpose**: Command-line tools and utilities

**Tool Choices**:
- CLI framework: click / typer / argparse
- Package manager: uv / poetry / pip

**Features**:
- Rich terminal output
- Config file support (TOML/YAML)
- Testing with pytest
- GitHub Actions CI/CD
- Docker containerization

**Structure**:
```
my-cli/
├── src/my_cli/
│   ├── __init__.py
│   ├── cli.py              # Main CLI entry point
│   └── commands/           # Subcommands
├── tests/
│   └── test_cli.py
├── pyproject.toml
├── README.md
└── .gitignore
```

**Special Features**:
- Auto-generates command groups
- Includes example subcommands
- Entry points configured in pyproject.toml

### 2. fastapi-api (Web APIs)

**Purpose**: REST APIs and web services

**Tool Choices**:
- Database: SQLAlchemy / raw SQL / none
- Package manager: uv / poetry / pip
- Async driver: asyncpg / aiomysql / none

**Features**:
- Database migrations (Alembic)
- JWT authentication
- API documentation (auto-generated)
- Docker + docker-compose
- Testing with pytest
- GitHub Actions CI/CD

**Structure**:
```
my-api/
├── app/
│   ├── main.py             # FastAPI app
│   ├── routers/            # API routes
│   ├── models/             # Database models
│   ├── schemas/            # Pydantic schemas
│   └── config.py           # Configuration
├── tests/
├── alembic/                # Database migrations
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
└── README.md
```

**Special Features**:
- Example CRUD endpoints
- Database session management
- Environment-based configuration
- Health check endpoints

### 3. python-package (Libraries)

**Purpose**: Reusable Python packages for distribution

**Tool Choices**:
- Package manager: uv / poetry / setuptools
- Documentation tool: Sphinx / MkDocs / none

**Features**:
- Testing with pytest
- Type stubs (py.typed)
- GitHub Actions (with PyPI publish workflow)
- Pre-commit hooks
- Changelog management

**Structure**:
```
my-package/
├── src/my_package/
│   ├── __init__.py         # With __version__
│   ├── py.typed            # Type stub marker
│   └── core.py
├── tests/
├── docs/
├── CHANGELOG.md
├── pyproject.toml
└── README.md
```

**Special Features**:
- Configured for PyPI distribution
- Version management
- Proper package metadata
- Publishing workflow

### 4. ml-project (ML/Data Science)

**Purpose**: Machine learning and data science projects

**Tool Choices**:
- Framework: pytorch / tensorflow / sklearn / none
- Notebook type: jupyter / jupyterlab
- Package manager: uv / poetry / pip

**Features**:
- Experiment tracking: MLflow / wandb / none
- Data versioning (DVC)
- Docker with GPU support
- Testing for data pipelines

**Structure**:
```
my-ml-project/
├── notebooks/              # Jupyter notebooks
│   └── 01_exploration.ipynb
├── data/
│   ├── raw/
│   └── processed/
├── models/                 # Saved models
├── src/                    # Reusable code
│   ├── data/
│   ├── features/
│   └── models/
├── tests/
├── requirements.txt
└── README.md
```

**Special Features**:
- .gitignore for large files
- Common imports in notebooks
- Requirements split (base/gpu)
- Experiment tracking setup

### 5. automation-script (Scripts & Automation)

**Purpose**: Task automation, scheduled jobs, data processing

**Tool Choices**:
- Scheduler: none / cron / APScheduler
- Config format: YAML / TOML / JSON / env
- Package manager: uv / poetry / pip

**Features**:
- Logging setup
- Error notifications (email/slack)
- Testing
- Docker containerization
- Systemd service file

**Structure**:
```
my-script/
├── src/my_script/
│   ├── runner.py           # Main script
│   ├── tasks/              # Task modules
│   └── config.py
├── config/
│   └── config.yaml
├── logs/
├── tests/
├── my-script.service       # Systemd service
└── README.md
```

**Special Features**:
- Logging configuration
- Error handling patterns
- Example scheduled tasks
- Service deployment files

### 6. docs-site (Documentation)

**Purpose**: Documentation websites and technical writing

**Tool Choices**:
- Generator: MkDocs / Sphinx / Docusaurus
- Theme: material / readthedocs / book
- Package manager: uv / poetry / pip

**Features**:
- API docs auto-generation
- GitHub Pages deployment
- Search functionality
- Versioning support
- PDF export

**Structure**:
```
my-docs/
├── docs/
│   ├── index.md
│   ├── getting-started.md
│   ├── api/
│   └── assets/
├── mkdocs.yml              # Or conf.py for Sphinx
├── .github/workflows/
│   └── deploy.yml
└── README.md
```

**Special Features**:
- Configured deployment workflow
- Theme customization
- Navigation structure
- Code documentation integration

## Implementation Details

### Core Components

**manifest.py**: Manifest parsing and validation
- Load YAML manifests
- Validate schema (required fields, valid types)
- Provide type-safe access to manifest data

**engine.py**: Project generation engine
- Orchestrate generation process
- Manage Jinja2 environment
- Execute post-generation actions
- Error handling and rollback

**interactive.py**: Interactive UI
- Display template options
- Collect user selections
- Validate selections
- Show preview of what will be generated

**renderers.py**: File rendering
- Jinja2 template rendering
- Context building from selections
- Conditional file generation
- Path transformations (project_name to snake_case, etc.)

**cli.py**: Click commands
- `pocket project init` command group
- `--list`, `--show`, `--quick` options
- Integration with existing pocket CLI

### Dependencies

**Required**:
- `click` - CLI interface (already in super-pocket)
- `rich` - Terminal UI (already in super-pocket)
- `jinja2` - Template rendering
- `pyyaml` - YAML parsing

**Optional**:
- `questionary` - Enhanced interactive prompts (alternative: use rich only)

### Error Handling

**Validation Errors**:
- Invalid manifest format
- Missing required fields
- Invalid template references
- Incompatible option combinations

**Runtime Errors**:
- Template file not found
- Jinja2 rendering errors
- Post-generation command failures
- Permission errors during file creation

**Recovery**:
- Clear error messages with context
- Suggestions for fixing issues
- Partial rollback on failure
- Dry-run mode to preview without creating files

## Testing Strategy

### Unit Tests
- Manifest parsing and validation
- Template rendering with various contexts
- Conditional logic evaluation
- File path transformations

### Integration Tests
- Full project generation for each template
- Post-generation action execution
- Interactive UI flow (mocked inputs)
- Error scenarios and recovery

### Template Tests
- Each template renders successfully
- All tool choice combinations work
- Feature toggles produce valid projects
- Generated projects are valid (imports work, tests pass)

## Future Enhancements

### Phase 1 (Initial Release)
- All 6 templates with basic customization
- Interactive UI
- Post-generation actions
- Comprehensive tests

### Phase 2 (Future)
- Custom template creation wizard
- Template validation CLI command
- Dry-run/preview mode
- Template sharing/import from URLs
- Variable substitution in post_generation commands
- Dependency conflict detection

### Phase 3 (Advanced)
- Web UI for template browsing
- Template marketplace
- Project update/migration (apply new template features to existing projects)
- Template composition (combine multiple templates)
- AI-assisted template generation

## Success Criteria

1. **Developer Productivity**: New projects initialize in < 1 minute with full setup
2. **Flexibility**: 80% of use cases covered by template + customization
3. **Quality**: Generated projects follow best practices (testing, linting, proper structure)
4. **Usability**: Interactive UI is intuitive, `--quick` mode is fast
5. **Maintainability**: Adding new templates is straightforward (< 1 hour for new template)
6. **Reliability**: Post-generation actions handle failures gracefully

## Conclusion

This project initialization tool addresses a real developer pain point: the tedious, repetitive setup of new Python projects. By combining the speed of templates with the flexibility of interactive customization, it provides the best of both worlds.

The declarative manifest approach makes templates easy to create, modify, and share. The six initial templates cover common Python development scenarios from CLI tools to ML projects. The extensible architecture allows for future growth while maintaining simplicity.

Next steps:
1. Implement core engine and manifest parser
2. Create interactive UI
3. Build first template (python-cli) as reference
4. Develop remaining 5 templates
5. Add comprehensive tests
6. Update documentation and examples
