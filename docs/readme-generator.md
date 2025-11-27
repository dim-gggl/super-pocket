# README Generator

Smart README creation with automatic project detection and a chill, friendly workflow.

## What it does

- **Detects the stack**: Language, framework, project type, and runtime version.
- **Writes the basics**: Clone/install/run, features, and contribution cues aligned to your stack.
- **Stays light**: No fluff—just the essentials you actually need to ship.

## Quick start (CLI)

```bash
# Analyze your project
pocket readme analyze -p .

# Generate README (one-shot)
pocket readme generate -p . -o README.md

# Wizard inside the project group
pocket project readme -p . -o README.md
```

## Under the hood

- **Detector**: `ProjectDetector` scans files (pyproject.toml, etc.) to infer type.
- **Generator**: `ReadmeGenerator` builds sections matched to the detected context.

## Current support

### Languages
- Python (pyproject.toml detection)

### Project types
- CLI tools
- Web applications
- Libraries

## Roadmap

- Section selection toggle
- Badge customization
- Multi-language support (JavaScript, Go, Rust)
- Smarter template choices
- Preview/edit UI
