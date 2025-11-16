# README Generator Design

**Date:** 2025-11-16
**Feature:** Smart README Generator for Super Pocket
**Purpose:** Generate focused READMEs that help developers clone → run → contribute

## Overview

### Vision

A smart README generator that detects project context (language, framework, type), offers user control through checklists and interactive editing, learns from preferences, and integrates with Super Pocket's existing tools.

**Core Principle:** READMEs are for running projects locally, not comprehensive documentation. Generate minimal but accurate content with essential commands only.

### User Flow

1. User runs `pocket readme generate` in a project directory
2. Analyzer scans project files to detect language/framework and project type
3. System asks 2-3 clarifying questions if detection is ambiguous
4. Generator produces baseline sections automatically
5. User selects badges and additional sections from checklists
6. Interactive preview shows rendered README with options: Save, Edit section, Regenerate, Cancel
7. Optional: Save choices as reusable template for future projects

## Smart Detection System

### Detection Strategy

**Language & Framework Detection:**
- **Python:** `pyproject.toml`, `setup.py`, `requirements.txt` → Check for Django/FastAPI/Flask imports
- **JavaScript/TypeScript:** `package.json` → Analyze dependencies for React/Vue/Express/Next.js
- **Go:** `go.mod` → Check for web frameworks (Gin, Echo, Fiber)
- **Rust:** `Cargo.toml` → Analyze dependencies for Actix/Rocket/CLI patterns
- **Java:** `pom.xml`, `build.gradle` → Detect Spring Boot, Maven/Gradle
- **Ruby:** `Gemfile` → Rails detection
- **PHP:** `composer.json` → Laravel/Symfony detection

**Project Type Detection:**
- **CLI Tool:** Presence of CLI frameworks (click, typer, commander, cobra), bin entries
- **Web App:** Web framework dependencies, templates/views directories
- **Library/Package:** Published to registry (PyPI, npm), no executable entry points
- **API Service:** REST/GraphQL frameworks, OpenAPI specs, routes/endpoints files

**Additional Context:**
- License: Read LICENSE file
- CI/CD: Check `.github/workflows/`, `.gitlab-ci.yml`
- Testing: Detect pytest, jest, go test configurations
- Documentation: Check for `docs/` directory, ReadTheDocs config
- Environment: Look for `.env.example`, `config/` directories
- Version: Extract from package metadata files

### Clarification Questions

Asked only when detection is ambiguous (max 2-3 questions):
- "I detected FastAPI - is this a REST API service or a web application?"
- "Multiple package managers found (npm, yarn, pnpm) - which is primary?"
- "Is this a published package or internal tool?"

Smart defaults pre-selected based on detection confidence.

## Content Generation

### Baseline Sections (Always Included)

**1. Project Title/Description**
- Extract from: package.json, pyproject.toml, Cargo.toml
- Fallback: Use directory name, ask user for one-line description

**2. Badges**
Present checklist of auto-detectable badges:
- Language/Runtime version (Python 3.11+, Node 18+)
- License (MIT, Apache, etc.)
- Build/CI status (GitHub Actions, GitLab CI)
- Package version (PyPI, npm, crates.io)
- Code coverage
- Documentation (ReadTheDocs, GitHub Pages)
- Downloads/Stars (for published packages)

User selects which to include.

**3. Prerequisites**
Auto-generate based on detection:
- Runtime version (Python 3.11+, Node 18+, Go 1.21+)
- System dependencies (PostgreSQL, Redis if detected)
- Package managers (pip/uv, npm/yarn, cargo)

**4. Installation**
Generate actual commands based on detected setup:
```bash
# Python example
git clone <repo-url>
cd project-name
uv sync  # or: pip install -e .
```

Use detected package manager preferences.

**5. Project Structure**
Generate tree view of key directories:
```
project/
├── src/           # Source code
├── tests/         # Test suite
├── docs/          # Documentation
└── config/        # Configuration files
```

Detect and describe actual project layout.

### Optional Sections (Checklist)

**For CLI Tools:**
- Commands Reference
- Usage Examples
- Configuration Options

**For Web Apps:**
- Configuration (Environment Variables)
- Running Locally (dev server commands)
- Database Setup
- Common Issues

**For Libraries/Packages:**
- Quick Start
- API Usage Examples
- Importing

**For APIs:**
- Endpoints Overview
- Running Locally
- API Documentation Link

**Universal Optional Sections:**
- Running Tests
- Development Setup
- Contributing Guidelines
- License

## Interactive Preview & Editing

### Preview Interface

After generation, display:
1. Rendered README using `pocket markdown render`
2. Section outline (numbered list)
3. Action menu:
   ```
   README Preview Generated

   Sections included:
   1. Project Title/Description
   2. Badges (3 selected)
   3. Prerequisites
   4. Installation
   5. Project Structure
   6. Commands Reference
   7. Running Tests

   What would you like to do?
   → Save README.md
   → Edit a section
   → Regenerate completely
   → Cancel
   ```

### Edit Section Flow

When user chooses "Edit a section":
1. Prompt: "Which section? (1-7)"
2. Show current content
3. Ask: "How would you like to edit?"
   - **Regenerate with new inputs** - Re-ask relevant questions
   - **Edit manually** - Open in $EDITOR
4. Return to preview with updated content
5. Can edit multiple sections before saving

### Save Behavior

When saving:
1. Check if README.md exists
2. If exists: Prompt "Overwrite, Backup (README.backup.md), or Merge?"
3. Write file
4. Prompt: "Save these settings as a template?"
   - If yes: Save to `~/.config/pocket/readme-templates/<name>.json`

### Post-Save Actions

After successful save:
```
✓ README.md created successfully

Would you also like to:
- View the rendered README
- Commit to git
- Nothing, I'm done
```

## Template System & Learning

### Template Storage

Location: `~/.config/pocket/readme-templates/`

```
readme-templates/
├── python-cli.json
├── fastapi-api.json
├── react-app.json
└── defaults.json          # Learned preferences per project type
```

### Template Structure

```json
{
  "name": "python-cli",
  "project_type": "cli",
  "language": "python",
  "badges": ["python-version", "license", "build-status"],
  "sections": [
    "title-description",
    "badges",
    "prerequisites",
    "installation",
    "project-structure",
    "commands-reference",
    "running-tests"
  ],
  "preferences": {
    "package_manager": "uv",
    "include_dev_setup": true,
    "testing_framework": "pytest"
  }
}
```

### Learning from History

**Smart defaults system:**
- Track user choices per project type in `defaults.json`
- After each generation, update preference weights
- Example: If user consistently excludes "Contributing Guidelines" for CLI tools, pre-uncheck it
- Never automatic - suggestions only, user always has final control

### Using Templates

**From interactive wizard:**
- At start: "Found matching template 'python-cli'. Use it? (Y/n)"
- If yes: Skip detection, load template, show preview immediately

**Direct template usage:**
```bash
pocket readme from-template python-cli
```

## CLI Command Suite

### Commands

**1. `pocket readme generate`**
- Default interactive wizard mode
- Flags:
  - `--template <name>` - Use saved template
  - `--auto` - Skip prompts, use smart defaults
  - `--output <file>` - Output to specific file (default: README.md)
  - `--no-backup` - Don't create backup of existing README

**2. `pocket readme from-template <name>`**
- Load specific template by name
- Fill in project-specific values
- Go directly to preview mode

**3. `pocket readme templates`**
- `list` - Show all saved templates
- `show <name>` - Display template configuration
- `delete <name>` - Remove a template
- `export <name>` - Export template as JSON
- `import <file>` - Import template from JSON

**4. `pocket readme analyze`**
- Show detection results without generating README
- Output example:
  ```
  Project Analysis:
  - Language: Python 3.11
  - Framework: FastAPI
  - Project Type: API Service
  - Package Manager: uv
  - Testing: pytest detected
  - CI/CD: GitHub Actions
  - License: MIT

  Suggested template: fastapi-api
  ```

**5. `pocket readme badges`**
- Update badges in existing README.md
- Interactive checklist to add/remove badges
- Preserves rest of README content

**6. `pocket readme update`**
- Smart update for existing READMEs
- Detect outdated sections
- Offer to regenerate specific sections while keeping custom content

## Technical Implementation

### Architecture

```
super_pocket/
├── readme/
│   ├── __init__.py
│   ├── cli.py                 # Click commands
│   ├── generator.py           # Main generation orchestrator
│   ├── detector.py            # Project detection logic
│   ├── templates/             # README section templates
│   │   ├── base.py           # Baseline sections
│   │   ├── cli_tools.py      # CLI-specific sections
│   │   ├── web_apps.py       # Web app sections
│   │   ├── libraries.py      # Library sections
│   │   └── apis.py           # API sections
│   ├── badges.py             # Badge generation
│   ├── preview.py            # Interactive preview/edit UI
│   ├── template_manager.py   # Template save/load/learning
│   └── analyzers/            # Language-specific analyzers
│       ├── python.py
│       ├── javascript.py
│       ├── go.py
│       ├── rust.py
│       └── ...
```

### Key Dependencies

**Existing:**
- `click` - CLI interface
- `rich` - Terminal UI and formatting
- `markdown` rendering (existing pocket feature)

**New:**
- `tomli` / `tomllib` - Parse TOML files (built-in for Python 3.11+)
- `pyyaml` - Parse YAML configs (if needed)
- `pathlib` - File system operations (built-in)

### Data Flow

1. **Detection Phase:** `detector.py` orchestrates analyzers → `ProjectContext` dataclass
2. **Question Phase:** Low-confidence detections trigger prompts → merge into `ProjectContext`
3. **Generation Phase:** Select templates based on type → generate markdown sections
4. **Preview/Edit Phase:** `rich` panels/menus → edit in $EDITOR → re-render
5. **Template/Learning Phase:** Save JSON, update defaults.json

### Testing Strategy

**Unit Tests:**
- Test each language analyzer independently
- Mock file system for detection tests
- Template rendering with fixture data

**Integration Tests:**
- Test full generation flow on sample projects
- Different project types generate correctly
- Template save/load/apply workflows

**Fixture Projects:**
- `tests/fixtures/` with sample projects for each type
- Python CLI, FastAPI API, React app, Go service, etc.

## Edge Cases & Error Handling

**Monorepos:**
- Detect multiple projects in subdirectories
- Prompt: "Multiple projects detected. Generate README for root or specific package?"

**Mixed Language Projects:**
- Backend + Frontend (e.g., FastAPI + React)
- Detect both, ask which is primary
- Option to generate sections for both

**No Detection Possible:**
- Fall back to manual template selection
- Offer generic templates: "Minimal", "Standard", "Comprehensive"

**Non-Standard Structures:**
- Graceful fallback to basic detection
- Allow manual override of all detected values

**Existing README:**
- Backup strategies: `.backup`, timestamped backups
- Merge mode: Preserve custom sections, update detected ones
- Diff preview before overwriting

## Integration with Super Pocket

**Leverage Existing Features:**
- Use `pocket markdown render` for README preview
- Integrate with `pocket project to-file`
- Templates stored alongside agent templates/cheatsheets
- Consistent CLI patterns

**Cross-Feature Synergy:**
- `pocket project to-file` could offer to generate README if missing
- `pocket templates init` could generate README for agent projects
- Badges link to documentation created with other pocket tools

## Success Metrics

- Developers can generate useful README in < 2 minutes
- Generated READMEs require minimal manual editing
- Detection accuracy > 90% for common project types
- Users create and reuse templates
- Reduced "how do I run this?" questions in projects

## Future Enhancements (Post-MVP)

**Phase 2 Features:**
- Visual README builder (TUI with live preview)
- Team templates (share via git repos)
- Multi-language support (English, Spanish, Chinese)
- README linting (analyze for missing sections, broken links)
- Auto-update monitoring

**Advanced Detection:**
- Docker integration
- Database migrations detection
- Monorepo intelligence (turborepo, nx, cargo workspaces)
- Framework-specific optimizations

## Documentation Needs

**User Documentation:**
- Tutorial: "Generating Your First README"
- Guide: "Understanding Project Detection"
- Reference: "All CLI Commands"
- Cookbook: "Custom Templates for Team Standards"

**Developer Documentation:**
- Adding new language analyzers
- Creating custom section templates
- Extending badge generation
