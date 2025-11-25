# Super Pocket

[![Documentation Status](https://readthedocs.org/projects/pocketdocs/badge/?version=latest)](https://pocketdocs.readthedocs.io/en/latest/?badge=latest)
[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

A collection of developer productivity tools including markdown rendering, project exporters, agent templates, and cheatsheets management.

**[📚 Read the Documentation](https://pocketdocs.readthedocs.io/en/latest/)** | [🚀 Quick Start](#quick-start) | [💡 Features](#features)

## Features

- **Markdown Rendering**: Beautiful terminal rendering of Markdown files with syntax highlighting
- **Project Export**: Convert entire projects to single Markdown files for easy sharing
- **Project Initialization**: Scaffold new projects with intelligent templates (6 types: python-cli, fastapi-api, python-package, ml-project, automation-script, docs-site)
- **Agent Templates**: Manage and distribute AI agent configuration templates
- **Cheatsheets**: Quick access to development cheatsheets
- **README Generator**: Smart README generation with project detection and templates
- **Unified CLI**: Single command-line interface for all tools

## Installation

### From Source

```bash
# Clone the repository
git clone <repository-url>
cd pocket

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package
pip install -e .

# Or with development dependencies
pip install -e ".[dev]"

# Or with specific features
pip install -e ".[pdf]"      # PDF conversion tools
pip install -e ".[web]"      # Web utilities
pip install -e ".[all]"      # All optional dependencies
```

### Using uv (recommended)

```bash
# Install dependencies
uv sync

# Install with optional dependencies
uv pip install -e ".[all]"

# Activate virtual environment
source .venv/bin/activate
```

## Quick Start

### Unified CLI

```bash
# View all available commands
pocket --help

# Render a markdown file
pocket markdown render README.md

# Export project to a single file
pocket project to-file -p . -o project.md

# List available templates and cheatsheets
pocket templates list

# View a cheatsheet
pocket templates view SQL -t cheatsheet

# Copy a template to your project
pocket templates copy unit_tests_agent -o .agents/

# Initialize agent templates directory
pocket templates init

# Convert text/markdown to PDF
pocket pdf convert document.md -o output.pdf

# Generate favicon from image
pocket web favicon logo.png -o favicon.ico

# Initialize a new Python CLI project
pocket project init new python-cli my-cli-tool --quick

# Initialize a FastAPI API project (interactive)
pocket project init new fastapi-api my-api

# List all available templates
pocket project init list

# View template details
pocket project init show ml-project
```

### Standalone Commands (Backward Compatible)

```bash
# Render markdown
markd README.md

# Export project
project to-file -p . -o output.md

# Convert to PDF
conv-to-pdf document.md output.pdf

# Generate favicon
flavicon logo.png -o favicon.ico
```

## Commands Reference

### Markdown Tools

```bash
# Render markdown file in terminal
pocket markdown render <file>
pocket markdown render README.md
```

### Project Tools

```bash
# Export entire project to single Markdown file
pocket project to-file [OPTIONS]

Options:
  -p, --path TEXT      Project directory (default: current directory)
  -o, --output TEXT    Output file name (default: <project_name>-1-file.md)
  -e, --exclude TEXT   Comma-separated list of files/dirs to exclude
```

Example:
```bash
pocket project to-file -p ./my-project -o export.md -e "node_modules,dist"
```

### Project Initialization

```bash
# List available project templates
pocket project init list

# Show details about a specific template
pocket project init show <template-name>

# Create a new project from a template
pocket project init new <template-name> [OPTIONS]

Options:
  -p, --path TEXT    Output directory for the new project
  -q, --quick        Skip interactive prompts, use defaults
```

**Available Templates:**

1. **python-cli** - Command-line tools
   - Tool choices: click/typer/argparse, uv/poetry/pip
   - Features: rich output, testing, GitHub Actions, Docker

2. **fastapi-api** - REST APIs with FastAPI
   - Tool choices: database (sqlite/postgres/mysql), auth (jwt/session/none)
   - Features: Alembic migrations, testing, Docker, CORS

3. **python-package** - PyPI-ready packages
   - Tool choices: package manager, build tool (hatchling/setuptools)
   - Features: testing, documentation (sphinx/mkdocs), type stubs, CI

4. **ml-project** - Machine learning projects
   - Tool choices: framework (pytorch/tensorflow/sklearn), experiment tracking
   - Features: Jupyter notebooks, DVC, Docker, GPU support

5. **automation-script** - Scheduled jobs and automation
   - Tool choices: scheduler (cron/apscheduler), config format (yaml/toml/json/env)
   - Features: logging, notifications, systemd, Docker

6. **docs-site** - Documentation websites
   - Tool choices: docs tool (sphinx/mkdocs/docusaurus), theme
   - Features: API docs, versioning, search, i18n, GitHub Pages

**Examples:**

```bash
# Create a CLI tool with default settings
pocket project init new python-cli my-tool --quick

# Create a FastAPI API with custom settings (interactive)
pocket project init new fastapi-api my-api
# You'll be prompted for database choice, auth method, features, etc.

# Create an ML project with specific path
pocket project init new ml-project --path ./projects/my-ml-project

# Create a documentation site
pocket project init new docs-site my-docs --quick
```

### Templates & Cheatsheets

```bash
# List all available items
pocket templates list
pocket templates list -t templates
pocket templates list -t cheatsheets

# View a template or cheatsheet
pocket templates view <name>
pocket templates view unit_tests_agent
pocket templates view SQL -t cheatsheet

# Copy to your project
pocket templates copy <name> -o <output-path>
pocket templates copy unit_tests_agent -o .agents/

# Initialize agent templates directory
pocket templates init
pocket templates init -o ./my-agents/
```

### README Generator

```bash
# Analyze project to see what would be detected
pocket readme analyze

# Generate a README for current project
pocket readme generate

# Generate with custom output path
pocket readme generate -o docs/README.md
```

## Project Structure

```
pocket/
├── .AGENTS/                     # Agent configurations for this project
├── super_pocket/                # Main package
│   ├── markdown/                # Markdown rendering tools
│   ├── project/                 # Project export tools
│   │   ├── init/                # Project initialization feature
│   │   │   ├── cli.py           # CLI commands
│   │   │   ├── engine.py        # Generation engine
│   │   │   ├── manifest.py      # Template manifest models
│   │   │   ├── renderers.py     # Jinja2 rendering
│   │   │   ├── actions.py       # Post-generation actions
│   │   │   └── interactive.py   # Interactive UI
│   │   └── templates/           # Project templates
│   │       ├── python-cli.yaml
│   │       ├── fastapi-api.yaml
│   │       ├── python-package.yaml
│   │       ├── ml-project.yaml
│   │       ├── automation-script.yaml
│   │       └── docs-site.yaml
│   ├── pdf/                     # PDF conversion
│   ├── web/                     # Web utilities
│   └── templates_and_cheatsheets/
│       ├── templates/           # Agent configuration templates
│       └── cheatsheets/         # Development cheatsheets
├── tests/                       # Test suite
├── docs/                        # Documentation
└── examples/                    # Usage examples
```

## Available Templates

### Agent Configuration Templates

- **agent_maker.md**: Agent creation assistant configuration
- **unit_tests_agent.md**: Comprehensive unit test generator configuration
- **agents_template_maker.md**: Template for generating AGENTS.md files
- **job_assistant_agent.md**: Job search and application assistant

### Cheatsheets

- **SQL.md**: SQL commands and queries reference

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pocket --cov-report=html

# Run specific test file
pytest tests/unit_tests/test_markdown/test_renderer.py
```

### Code Quality

```bash
# Format code with black
black pocket tests

# Lint with ruff
ruff check pocket tests

# Type checking (if using mypy)
mypy pocket
```

### Adding New Tools

1. Create a new module in `pocket/`
2. Implement functionality with proper type hints and docstrings
3. Add CLI commands to `pocket/cli.py`
4. Create tests in `tests/unit_tests/`
5. Update this README

### Adding Templates or Cheatsheets

1. Add `.md` files to `pocket/templates_and_cheatsheets/templates/` or `cheatsheets/`
2. Ensure proper markdown formatting
3. Test with `pocket templates view <name>`

## Configuration

### Agent Configurations

Agent configurations for **this project** are stored in `.AGENTS/`:

- `AGENTS.md`: Main agent configuration and project rules
- `Agent_maker.md`: Agent creation assistant
- `Unit_tests_agent.md`: Unit test generation configuration
- Other agent-specific configurations

### Environment

The project uses:
- Python 3.11+
- `click` for CLI interfaces
- `rich` for enhanced terminal output
- `pytest` for testing

### Optional Dependencies

- **PDF features**: `fpdf2`, `markdown-pdf`
- **Web features**: `Pillow` for favicon generation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Ensure all tests pass
5. Submit a pull request

## License

[Add your license here]

## Author

dim-gggl

## Changelog

### v0.1.0 (Current)

- Initial unified structure
- Markdown rendering tools
- Project-to-file exporter
- Agent templates management
- Cheatsheets system
- PDF conversion tools (text and Markdown)
- Favicon generation utilities
- **Project initialization with 6 intelligent templates**
  - python-cli: Command-line tools with Click/Typer/argparse
  - fastapi-api: REST APIs with database and auth
  - python-package: PyPI-ready packages with proper structure
  - ml-project: ML workflows with PyTorch/TensorFlow/sklearn
  - automation-script: Scheduled jobs with cron/APScheduler
  - docs-site: Documentation with Sphinx/MkDocs/Docusaurus
- Comprehensive test suite (94 tests)
- Unified CLI interface
- Backward-compatible standalone commands

## Roadmap

- [x] PDF conversion tools ✅
- [x] Favicon generation utilities ✅
- [x] Project initialization with intelligent templates ✅
- [ ] Additional cheatsheets (Git, Docker, Python, etc.)
- [ ] Template validation in CLI
- [ ] Interactive template creation wizard
- [ ] Package publishing to PyPI
- [ ] Web-based template browser
- [ ] More PDF output formats
- [ ] Image optimization tools

## Support

For issues, questions, or contributions, please [open an issue](https://github.com/your-username/pocket/issues).

---

**Happy Coding!** 🚀
