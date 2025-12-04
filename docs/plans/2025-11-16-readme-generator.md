# README Generator Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a smart README generator that detects project context and creates focused "clone → run → contribute" READMEs.

**Architecture:** Detection layer (language-specific analyzers) → Generation layer (template-based sections) → Interactive layer (preview/edit UI) → Persistence layer (template manager). CLI orchestrates all flows.

**Tech Stack:** Python 3.11+, Click (CLI), Rich (UI), tomllib (TOML parsing), pathlib, JSON

---

## Task 1: Project Structure and Core Data Models

**Files:**
- Create: `super_pocket/readme/__init__.py`
- Create: `super_pocket/readme/models.py`
- Create: `tests/unit_tests/test_readme/__init__.py`
- Create: `tests/unit_tests/test_readme/test_models.py`

**Step 1: Write the failing test for ProjectContext model**

Create `tests/unit_tests/test_readme/test_models.py`:

```python
"""Tests for README generator data models."""

import pytest
from pathlib import Path
from src.super_pocket.readme.models import ProjectContext, ProjectType


def test_project_context_creation():
    """Test creating a ProjectContext with basic data."""
    context = ProjectContext(
        project_name="test-project",
        project_path=Path("/test/path"),
        language="python",
        project_type=ProjectType.CLI_TOOL
    )

    assert context.project_name == "test-project"
    assert context.language == "python"
    assert context.project_type == ProjectType.CLI_TOOL


def test_project_context_with_optional_fields():
    """Test ProjectContext with optional fields."""
    context = ProjectContext(
        project_name="test-project",
        project_path=Path("/test/path"),
        language="python",
        project_type=ProjectType.WEB_APP,
        framework="fastapi",
        package_manager="uv",
        license_type="MIT"
    )

    assert context.framework == "fastapi"
    assert context.package_manager == "uv"
    assert context.license_type == "MIT"


def test_project_type_enum_values():
    """Test ProjectType enum has expected values."""
    assert ProjectType.CLI_TOOL.value == "cli"
    assert ProjectType.WEB_APP.value == "web_app"
    assert ProjectType.LIBRARY.value == "library"
    assert ProjectType.API.value == "api"
```

**Step 2: Create test __init__.py**

Create `tests/unit_tests/test_readme/__init__.py`:

```python
"""Tests for README generator module."""
```

**Step 3: Run test to verify it fails**

Run: `cd /Users/dim-gggl/~/Dev\ Tools/Fancy_Tools/.worktrees/readme-generator && source .venv/bin/activate && pytest tests/unit_tests/test_readme/test_models.py -v`

Expected: FAIL with "No module named 'super_pocket.readme'"

**Step 4: Write minimal implementation**

Create `super_pocket/readme/__init__.py`:

```python
"""README generator for Super Pocket."""

__version__ = "0.1.0"
```

Create `super_pocket/readme/models.py`:

```python
"""Data models for README generator."""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional, List, Dict, Any


class ProjectType(Enum):
    """Types of projects."""
    CLI_TOOL = "cli"
    WEB_APP = "web_app"
    LIBRARY = "library"
    API = "api"


@dataclass
class ProjectContext:
    """Context information about a project for README generation."""

    # Required fields
    project_name: str
    project_path: Path
    language: str
    project_type: ProjectType

    # Optional detection results
    framework: Optional[str] = None
    package_manager: Optional[str] = None
    license_type: Optional[str] = None
    version: Optional[str] = None
    description: Optional[str] = None

    # Environment info
    runtime_version: Optional[str] = None
    has_tests: bool = False
    test_framework: Optional[str] = None
    has_ci: bool = False
    ci_platform: Optional[str] = None
    has_docs: bool = False

    # Dependencies
    dependencies: List[str] = field(default_factory=list)
    dev_dependencies: List[str] = field(default_factory=list)
    system_dependencies: List[str] = field(default_factory=list)

    # Detection confidence (0.0 to 1.0)
    confidence: float = 1.0

    # Additional metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
```

**Step 5: Run test to verify it passes**

Run: `cd /Users/dim-gggl/~/Dev\ Tools/Fancy_Tools/.worktrees/readme-generator && source .venv/bin/activate && pytest tests/unit_tests/test_readme/test_models.py -v`

Expected: PASS (3 tests)

**Step 6: Commit**

```bash
cd /Users/dim-gggl/~/Dev\ Tools/Fancy_Tools/.worktrees/readme-generator
git add super_pocket/readme/ tests/unit_tests/test_readme/
git commit -m "feat(readme): add core data models for project context

- Add ProjectType enum for project categorization
- Add ProjectContext dataclass with detection fields
- Add comprehensive tests for data models

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 2: Python Project Analyzer

**Files:**
- Create: `super_pocket/readme/analyzers/__init__.py`
- Create: `super_pocket/readme/analyzers/python.py`
- Create: `tests/unit_tests/test_readme/test_analyzers/__init__.py`
- Create: `tests/unit_tests/test_readme/test_analyzers/test_python.py`
- Create: `tests/fixtures/sample_projects/python_cli/pyproject.toml` (test fixture)

**Step 1: Write the failing test for Python analyzer**

Create `tests/fixtures/sample_projects/python_cli/pyproject.toml`:

```toml
[project]
name = "test-cli-tool"
version = "1.0.0"
description = "A test CLI tool"
requires-python = ">=3.11"
dependencies = [
    "click>=8.0.0",
]

[project.scripts]
testcli = "testcli.main:cli"
```

Create `tests/unit_tests/test_readme/test_analyzers/__init__.py`:

```python
"""Tests for project analyzers."""
```

Create `tests/unit_tests/test_readme/test_analyzers/test_python.py`:

```python
"""Tests for Python project analyzer."""

import pytest
from pathlib import Path
from src.super_pocket.readme.analyzers.python import PythonAnalyzer
from src.super_pocket.readme.models import ProjectType


@pytest.fixture
def python_cli_project(tmp_path):
    """Create a temporary Python CLI project."""
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("""[project]
name = "test-cli-tool"
version = "1.0.0"
description = "A test CLI tool"
requires-python = ">=3.11"
dependencies = [
    "click>=8.0.0",
]

[project.scripts]
testcli = "testcli.main:cli"
""")
    return tmp_path


def test_python_analyzer_detects_cli_tool(python_cli_project):
    """Test that Python analyzer detects CLI tools."""
    analyzer = PythonAnalyzer()
    context = analyzer.analyze(python_cli_project)

    assert context.language == "python"
    assert context.project_type == ProjectType.CLI_TOOL
    assert context.project_name == "test-cli-tool"
    assert context.description == "A test CLI tool"
    assert context.version == "1.0.0"
    assert context.runtime_version == ">=3.11"


def test_python_analyzer_detects_dependencies(python_cli_project):
    """Test that analyzer extracts dependencies."""
    analyzer = PythonAnalyzer()
    context = analyzer.analyze(python_cli_project)

    assert "click>=8.0.0" in context.dependencies


def test_python_analyzer_no_pyproject(tmp_path):
    """Test analyzer returns None when no pyproject.toml exists."""
    analyzer = PythonAnalyzer()
    context = analyzer.analyze(tmp_path)

    assert context is None
```

**Step 2: Run test to verify it fails**

Run: `cd /Users/dim-gggl/~/Dev\ Tools/Fancy_Tools/.worktrees/readme-generator && source .venv/bin/activate && pytest tests/unit_tests/test_readme/test_analyzers/test_python.py -v`

Expected: FAIL with "No module named 'super_pocket.readme.analyzers'"

**Step 3: Write minimal implementation**

Create `super_pocket/readme/analyzers/__init__.py`:

```python
"""Project analyzers for different languages."""

from .python import PythonAnalyzer

__all__ = ["PythonAnalyzer"]
```

Create `super_pocket/readme/analyzers/python.py`:

```python
"""Python project analyzer."""

import tomllib
from pathlib import Path
from typing import Optional
from ..models import ProjectContext, ProjectType


class PythonAnalyzer:
    """Analyze Python projects to extract context."""

    def analyze(self, project_path: Path) -> Optional[ProjectContext]:
        """
        Analyze a Python project.

        Args:
            project_path: Path to the project directory

        Returns:
            ProjectContext if Python project detected, None otherwise
        """
        pyproject_path = project_path / "pyproject.toml"

        if not pyproject_path.exists():
            return None

        try:
            with open(pyproject_path, "rb") as f:
                data = tomllib.load(f)
        except Exception:
            return None

        project_data = data.get("project", {})

        # Extract basic info
        project_name = project_data.get("name", project_path.name)
        description = project_data.get("description")
        version = project_data.get("version")
        runtime_version = project_data.get("requires-python")

        # Detect project type
        project_type = self._detect_project_type(project_data, data)

        # Extract dependencies
        dependencies = project_data.get("dependencies", [])

        return ProjectContext(
            project_name=project_name,
            project_path=project_path,
            language="python",
            project_type=project_type,
            description=description,
            version=version,
            runtime_version=runtime_version,
            dependencies=dependencies
        )

    def _detect_project_type(
        self,
        project_data: dict,
        full_data: dict
    ) -> ProjectType:
        """Detect the type of Python project."""
        # Check for CLI tool indicators
        if "scripts" in project_data or "entry_points" in project_data:
            return ProjectType.CLI_TOOL

        # Check for web framework dependencies
        deps = project_data.get("dependencies", [])
        deps_str = " ".join(deps).lower()

        if any(fw in deps_str for fw in ["fastapi", "flask", "django"]):
            return ProjectType.WEB_APP

        # Default to library
        return ProjectType.LIBRARY
```

**Step 4: Run test to verify it passes**

Run: `cd /Users/dim-gggl/~/Dev\ Tools/Fancy_Tools/.worktrees/readme-generator && source .venv/bin/activate && pytest tests/unit_tests/test_readme/test_analyzers/test_python.py -v`

Expected: PASS (3 tests)

**Step 5: Commit**

```bash
cd /Users/dim-gggl/~/Dev\ Tools/Fancy_Tools/.worktrees/readme-generator
git add super_pocket/readme/analyzers/ tests/unit_tests/test_readme/test_analyzers/ tests/fixtures/
git commit -m "feat(readme): add Python project analyzer

- Parse pyproject.toml for project metadata
- Detect CLI tools vs libraries vs web apps
- Extract dependencies and runtime version
- Add comprehensive tests with fixtures

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 3: Main Project Detector

**Files:**
- Create: `super_pocket/readme/detector.py`
- Create: `tests/unit_tests/test_readme/test_detector.py`

**Step 1: Write the failing test for detector**

Create `tests/unit_tests/test_readme/test_detector.py`:

```python
"""Tests for main project detector."""

import pytest
from pathlib import Path
from src.super_pocket.readme.detector import ProjectDetector
from src.super_pocket.readme.models import ProjectType


@pytest.fixture
def python_project(tmp_path):
    """Create a temporary Python project."""
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("""[project]
name = "test-project"
version = "1.0.0"
requires-python = ">=3.11"
dependencies = ["click>=8.0.0"]

[project.scripts]
test = "test.main:cli"
""")
    return tmp_path


def test_detector_finds_python_project(python_project):
    """Test detector successfully identifies Python project."""
    detector = ProjectDetector()
    context = detector.detect(python_project)

    assert context is not None
    assert context.language == "python"
    assert context.project_type == ProjectType.CLI_TOOL


def test_detector_returns_none_for_unknown(tmp_path):
    """Test detector returns None for unrecognized projects."""
    detector = ProjectDetector()
    context = detector.detect(tmp_path)

    assert context is None


def test_detector_uses_multiple_analyzers(python_project):
    """Test that detector tries multiple analyzers."""
    detector = ProjectDetector()
    # Should try all analyzers but find Python
    context = detector.detect(python_project)

    assert context.language == "python"
```

**Step 2: Run test to verify it fails**

Run: `cd /Users/dim-gggl/~/Dev\ Tools/Fancy_Tools/.worktrees/readme-generator && source .venv/bin/activate && pytest tests/unit_tests/test_readme/test_detector.py -v`

Expected: FAIL with "No module named 'super_pocket.readme.detector'"

**Step 3: Write minimal implementation**

Create `super_pocket/readme/detector.py`:

```python
"""Main project detector that orchestrates all analyzers."""

from pathlib import Path
from typing import Optional
from .models import ProjectContext
from .analyzers import PythonAnalyzer


class ProjectDetector:
    """Detect project language and type using multiple analyzers."""

    def __init__(self):
        """Initialize detector with all available analyzers."""
        self.analyzers = [
            PythonAnalyzer(),
            # Future: JavaScriptAnalyzer(), GoAnalyzer(), etc.
        ]

    def detect(self, project_path: Path) -> Optional[ProjectContext]:
        """
        Detect project context by trying all analyzers.

        Args:
            project_path: Path to the project directory

        Returns:
            ProjectContext if detected, None otherwise
        """
        if not project_path.exists() or not project_path.is_dir():
            return None

        # Try each analyzer in order
        for analyzer in self.analyzers:
            context = analyzer.analyze(project_path)
            if context is not None:
                return context

        return None
```

**Step 4: Run test to verify it passes**

Run: `cd /Users/dim-gggl/~/Dev\ Tools/Fancy_Tools/.worktrees/readme-generator && source .venv/bin/activate && pytest tests/unit_tests/test_readme/test_detector.py -v`

Expected: PASS (3 tests)

**Step 5: Commit**

```bash
cd /Users/dim-gggl/~/Dev\ Tools/Fancy_Tools/.worktrees/readme-generator
git add super_pocket/readme/detector.py tests/unit_tests/test_readme/test_detector.py
git commit -m "feat(readme): add main project detector

- Orchestrate multiple language analyzers
- Try analyzers in sequence until match found
- Extensible design for adding new analyzers

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 4: Badge Generator

**Files:**
- Create: `super_pocket/readme/badges.py`
- Create: `tests/unit_tests/test_readme/test_badges.py`

**Step 1: Write the failing test for badge generator**

Create `tests/unit_tests/test_readme/test_badges.py`:

```python
"""Tests for badge generator."""

import pytest
from pathlib import Path
from src.super_pocket.readme.badges import BadgeGenerator, BadgeType
from src.super_pocket.readme.models import ProjectContext, ProjectType


@pytest.fixture
def python_context():
    """Create a Python project context."""
    return ProjectContext(
        project_name="test-project",
        project_path=Path("/test"),
        language="python",
        project_type=ProjectType.CLI_TOOL,
        runtime_version=">=3.11",
        license_type="MIT"
    )


def test_badge_generator_available_badges(python_context):
    """Test getting available badges for a project."""
    generator = BadgeGenerator()
    badges = generator.get_available_badges(python_context)

    assert BadgeType.PYTHON_VERSION in badges
    assert BadgeType.LICENSE in badges


def test_badge_generator_python_version(python_context):
    """Test generating Python version badge."""
    generator = BadgeGenerator()
    markdown = generator.generate_badge(BadgeType.PYTHON_VERSION, python_context)

    assert "python-3.11" in markdown
    assert "badge" in markdown
    assert "shields.io" in markdown


def test_badge_generator_license_badge(python_context):
    """Test generating license badge."""
    generator = BadgeGenerator()
    markdown = generator.generate_badge(BadgeType.LICENSE, python_context)

    assert "MIT" in markdown
    assert "badge" in markdown


def test_badge_generator_skips_unavailable(python_context):
    """Test that unavailable badges return None."""
    python_context.has_ci = False
    generator = BadgeGenerator()

    # CI badge should not be available
    badges = generator.get_available_badges(python_context)
    assert BadgeType.BUILD_STATUS not in badges
```

**Step 2: Run test to verify it fails**

Run: `cd /Users/dim-gggl/~/Dev\ Tools/Fancy_Tools/.worktrees/readme-generator && source .venv/bin/activate && pytest tests/unit_tests/test_readme/test_badges.py -v`

Expected: FAIL with "No module named 'super_pocket.readme.badges'"

**Step 3: Write minimal implementation**

Create `super_pocket/readme/badges.py`:

```python
"""Badge generation for README files."""

from enum import Enum
from typing import List, Optional
from .models import ProjectContext


class BadgeType(Enum):
    """Types of badges that can be generated."""
    PYTHON_VERSION = "python_version"
    NODE_VERSION = "node_version"
    LICENSE = "license"
    BUILD_STATUS = "build_status"
    COVERAGE = "coverage"
    DOCS = "docs"
    PACKAGE_VERSION = "package_version"


class BadgeGenerator:
    """Generate badge markdown for README files."""

    def get_available_badges(self, context: ProjectContext) -> List[BadgeType]:
        """
        Get list of badges that can be generated for this project.

        Args:
            context: Project context

        Returns:
            List of available badge types
        """
        badges = []

        # Language version badges
        if context.language == "python" and context.runtime_version:
            badges.append(BadgeType.PYTHON_VERSION)
        elif context.language == "javascript" and context.runtime_version:
            badges.append(BadgeType.NODE_VERSION)

        # License badge
        if context.license_type:
            badges.append(BadgeType.LICENSE)

        # CI/CD badge
        if context.has_ci:
            badges.append(BadgeType.BUILD_STATUS)

        # Coverage badge
        if context.has_tests:
            badges.append(BadgeType.COVERAGE)

        # Documentation badge
        if context.has_docs:
            badges.append(BadgeType.DOCS)

        return badges

    def generate_badge(
        self,
        badge_type: BadgeType,
        context: ProjectContext
    ) -> Optional[str]:
        """
        Generate markdown for a specific badge.

        Args:
            badge_type: Type of badge to generate
            context: Project context

        Returns:
            Badge markdown or None if not available
        """
        if badge_type == BadgeType.PYTHON_VERSION:
            return self._python_version_badge(context)
        elif badge_type == BadgeType.LICENSE:
            return self._license_badge(context)
        elif badge_type == BadgeType.BUILD_STATUS:
            return self._build_status_badge(context)

        return None

    def _python_version_badge(self, context: ProjectContext) -> str:
        """Generate Python version badge."""
        version = context.runtime_version or "3.11+"
        # Extract major.minor from version string like ">=3.11"
        version_num = version.replace(">=", "").replace(">", "").strip()

        return (
            f"[![Python Version](https://img.shields.io/badge/"
            f"python-{version_num}%2B-blue.svg)]"
            f"(https://www.python.org/downloads/)"
        )

    def _license_badge(self, context: ProjectContext) -> str:
        """Generate license badge."""
        license_type = context.license_type or "MIT"

        return (
            f"[![License: {license_type}]"
            f"(https://img.shields.io/badge/License-{license_type}-green.svg)]"
            f"(https://opensource.org/licenses/{license_type})"
        )

    def _build_status_badge(self, context: ProjectContext) -> str:
        """Generate build status badge."""
        # Placeholder - would need repo info
        return (
            f"[![Build Status](https://img.shields.io/github/actions/"
            f"workflow/status/USER/REPO/ci.yml?branch=main)]"
            f"(https://github.com/USER/REPO/actions)"
        )
```

**Step 4: Run test to verify it passes**

Run: `cd /Users/dim-gggl/~/Dev\ Tools/Fancy_Tools/.worktrees/readme-generator && source .venv/bin/activate && pytest tests/unit_tests/test_readme/test_badges.py -v`

Expected: PASS (4 tests)

**Step 5: Commit**

```bash
cd /Users/dim-gggl/~/Dev\ Tools/Fancy_Tools/.worktrees/readme-generator
git add super_pocket/readme/badges.py tests/unit_tests/test_readme/test_badges.py
git commit -m "feat(readme): add badge generator

- Generate shields.io badges for Python, license, CI
- Detect available badges based on project context
- Support multiple badge types

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 5: README Section Templates

**Files:**
- Create: `super_pocket/readme/templates/__init__.py`
- Create: `super_pocket/readme/templates/base.py`
- Create: `super_pocket/readme/templates/cli_tools.py`
- Create: `tests/unit_tests/test_readme/test_templates/__init__.py`
- Create: `tests/unit_tests/test_readme/test_templates/test_base.py`

**Step 1: Write the failing test for base templates**

Create `tests/unit_tests/test_readme/test_templates/__init__.py`:

```python
"""Tests for README templates."""
```

Create `tests/unit_tests/test_readme/test_templates/test_base.py`:

```python
"""Tests for base README templates."""

import pytest
from pathlib import Path
from src.super_pocket.readme.templates.base import (
    TitleSection,
    PrerequisitesSection,
    InstallationSection
)
from src.super_pocket.readme.models import ProjectContext, ProjectType


@pytest.fixture
def python_cli_context():
    """Create a Python CLI project context."""
    return ProjectContext(
        project_name="test-cli",
        project_path=Path("/test"),
        language="python",
        project_type=ProjectType.CLI_TOOL,
        description="A test CLI tool",
        runtime_version=">=3.11",
        package_manager="uv",
        dependencies=["click>=8.0.0"]
    )


def test_title_section_generation(python_cli_context):
    """Test title section generation."""
    section = TitleSection()
    content = section.generate(python_cli_context)

    assert "# test-cli" in content
    assert "A test CLI tool" in content


def test_prerequisites_section(python_cli_context):
    """Test prerequisites section generation."""
    section = PrerequisitesSection()
    content = section.generate(python_cli_context)

    assert "## Prerequisites" in content
    assert "Python 3.11" in content or ">=3.11" in content


def test_installation_section(python_cli_context):
    """Test installation section generation."""
    section = InstallationSection()
    content = section.generate(python_cli_context)

    assert "## Installation" in content
    assert "uv sync" in content or "pip install" in content
    assert "```bash" in content
```

**Step 2: Run test to verify it fails**

Run: `cd /Users/dim-gggl/~/Dev\ Tools/Fancy_Tools/.worktrees/readme-generator && source .venv/bin/activate && pytest tests/unit_tests/test_readme/test_templates/test_base.py -v`

Expected: FAIL with "No module named 'super_pocket.readme.templates'"

**Step 3: Write minimal implementation**

Create `super_pocket/readme/templates/__init__.py`:

```python
"""README section templates."""

from .base import TitleSection, PrerequisitesSection, InstallationSection

__all__ = [
    "TitleSection",
    "PrerequisitesSection",
    "InstallationSection"
]
```

Create `super_pocket/readme/templates/base.py`:

```python
"""Base README sections that are included in all READMEs."""

from abc import ABC, abstractmethod
from typing import List
from ..models import ProjectContext


class Section(ABC):
    """Base class for README sections."""

    @abstractmethod
    def generate(self, context: ProjectContext) -> str:
        """Generate the section content."""
        pass


class TitleSection(Section):
    """Generate project title and description section."""

    def generate(self, context: ProjectContext) -> str:
        """Generate title section."""
        lines = [f"# {context.project_name}"]

        if context.description:
            lines.append("")
            lines.append(context.description)

        return "\n".join(lines)


class PrerequisitesSection(Section):
    """Generate prerequisites section."""

    def generate(self, context: ProjectContext) -> str:
        """Generate prerequisites section."""
        lines = ["## Prerequisites"]
        lines.append("")

        # Runtime version
        if context.runtime_version:
            if context.language == "python":
                version = context.runtime_version.replace(">=", "")
                lines.append(f"- Python {version}+")
            elif context.language == "javascript":
                lines.append(f"- Node.js {context.runtime_version}+")

        # Package manager
        if context.package_manager:
            lines.append(f"- {context.package_manager}")

        # System dependencies
        for dep in context.system_dependencies:
            lines.append(f"- {dep}")

        return "\n".join(lines)


class InstallationSection(Section):
    """Generate installation instructions section."""

    def generate(self, context: ProjectContext) -> str:
        """Generate installation section."""
        lines = ["## Installation"]
        lines.append("")
        lines.append("```bash")
        lines.append("# Clone the repository")
        lines.append(f"git clone <repository-url>")
        lines.append(f"cd {context.project_name}")
        lines.append("")

        # Language-specific installation
        if context.language == "python":
            if context.package_manager == "uv":
                lines.append("# Install dependencies with uv")
                lines.append("uv sync")
            else:
                lines.append("# Create virtual environment")
                lines.append("python -m venv .venv")
                lines.append("source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate")
                lines.append("")
                lines.append("# Install package")
                lines.append("pip install -e .")

        lines.append("```")

        return "\n".join(lines)


class ProjectStructureSection(Section):
    """Generate project structure section."""

    def generate(self, context: ProjectContext) -> str:
        """Generate project structure section."""
        lines = ["## Project Structure"]
        lines.append("")
        lines.append("```")
        lines.append(f"{context.project_name}/")

        # Basic structure based on language
        if context.language == "python":
            pkg_name = context.project_name.replace("-", "_")
            lines.append(f"├── {pkg_name}/        # Source code")
            lines.append(f"├── tests/            # Test suite")
            if context.has_docs:
                lines.append(f"├── docs/             # Documentation")
            lines.append(f"└── pyproject.toml    # Project configuration")

        lines.append("```")

        return "\n".join(lines)
```

**Step 4: Run test to verify it passes**

Run: `cd /Users/dim-gggl/~/Dev\ Tools/Fancy_Tools/.worktrees/readme-generator && source .venv/bin/activate && pytest tests/unit_tests/test_readme/test_templates/test_base.py -v`

Expected: PASS (3 tests)

**Step 5: Commit**

```bash
cd /Users/dim-gggl/~/Dev\ Tools/Fancy_Tools/.worktrees/readme-generator
git add super_pocket/readme/templates/ tests/unit_tests/test_readme/test_templates/
git commit -m "feat(readme): add base section templates

- Title/description section
- Prerequisites section with runtime and dependencies
- Installation section with language-specific commands
- Project structure section
- Abstract Section base class for extensibility

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 6: README Generator Core

**Files:**
- Create: `super_pocket/readme/generator.py`
- Create: `tests/unit_tests/test_readme/test_generator.py`

**Step 1: Write the failing test for generator**

Create `tests/unit_tests/test_readme/test_generator.py`:

```python
"""Tests for README generator core."""

import pytest
from pathlib import Path
from src.super_pocket.readme.generator import ReadmeGenerator
from src.super_pocket.readme.models import ProjectContext, ProjectType


@pytest.fixture
def python_context():
    """Create a Python project context."""
    return ProjectContext(
        project_name="test-project",
        project_path=Path("/test"),
        language="python",
        project_type=ProjectType.CLI_TOOL,
        description="A test project",
        runtime_version=">=3.11",
        package_manager="uv"
    )


def test_generator_creates_readme(python_context):
    """Test that generator creates README content."""
    generator = ReadmeGenerator()
    content = generator.generate(python_context, selected_badges=[], selected_sections=[])

    assert "# test-project" in content
    assert "A test project" in content


def test_generator_includes_baseline_sections(python_context):
    """Test that baseline sections are always included."""
    generator = ReadmeGenerator()
    content = generator.generate(python_context, selected_badges=[], selected_sections=[])

    # Baseline sections
    assert "# test-project" in content  # Title
    assert "Prerequisites" in content
    assert "Installation" in content


def test_generator_includes_optional_sections(python_context):
    """Test that optional sections are included when requested."""
    generator = ReadmeGenerator()
    content = generator.generate(
        python_context,
        selected_badges=[],
        selected_sections=["running-tests"]
    )

    assert "Running Tests" in content or "Tests" in content
```

**Step 2: Run test to verify it fails**

Run: `cd /Users/dim-gggl/~/Dev\ Tools/Fancy_Tools/.worktrees/readme-generator && source .venv/bin/activate && pytest tests/unit_tests/test_readme/test_generator.py -v`

Expected: FAIL with "No module named 'super_pocket.readme.generator'"

**Step 3: Write minimal implementation**

Create `super_pocket/readme/generator.py`:

```python
"""Main README generator."""

from typing import List
from .models import ProjectContext
from .templates.base import (
    TitleSection,
    PrerequisitesSection,
    InstallationSection,
    ProjectStructureSection
)
from .badges import BadgeGenerator, BadgeType


class ReadmeGenerator:
    """Generate README files from project context."""

    def __init__(self):
        """Initialize generator with section templates."""
        self.badge_generator = BadgeGenerator()

        # Baseline sections (always included)
        self.baseline_sections = {
            "title": TitleSection(),
            "prerequisites": PrerequisitesSection(),
            "installation": InstallationSection(),
            "structure": ProjectStructureSection()
        }

        # Optional sections
        self.optional_sections = {
            "running-tests": self._running_tests_section,
        }

    def generate(
        self,
        context: ProjectContext,
        selected_badges: List[BadgeType],
        selected_sections: List[str]
    ) -> str:
        """
        Generate README content.

        Args:
            context: Project context
            selected_badges: List of badge types to include
            selected_sections: List of optional section IDs to include

        Returns:
            Complete README markdown content
        """
        sections = []

        # Title section
        sections.append(self.baseline_sections["title"].generate(context))
        sections.append("")

        # Badges
        if selected_badges:
            badge_lines = []
            for badge_type in selected_badges:
                badge_md = self.badge_generator.generate_badge(badge_type, context)
                if badge_md:
                    badge_lines.append(badge_md)

            if badge_lines:
                sections.append(" ".join(badge_lines))
                sections.append("")

        # Baseline sections
        sections.append(self.baseline_sections["prerequisites"].generate(context))
        sections.append("")
        sections.append(self.baseline_sections["installation"].generate(context))
        sections.append("")
        sections.append(self.baseline_sections["structure"].generate(context))
        sections.append("")

        # Optional sections
        for section_id in selected_sections:
            if section_id in self.optional_sections:
                section_func = self.optional_sections[section_id]
                sections.append(section_func(context))
                sections.append("")

        return "\n".join(sections)

    def _running_tests_section(self, context: ProjectContext) -> str:
        """Generate running tests section."""
        lines = ["## Running Tests"]
        lines.append("")
        lines.append("```bash")

        if context.language == "python":
            if context.test_framework == "pytest":
                lines.append("pytest")
            else:
                lines.append("python -m pytest")

        lines.append("```")

        return "\n".join(lines)
```

**Step 4: Run test to verify it passes**

Run: `cd /Users/dim-gggl/~/Dev\ Tools/Fancy_Tools/.worktrees/readme-generator && source .venv/bin/activate && pytest tests/unit_tests/test_readme/test_generator.py -v`

Expected: PASS (3 tests)

**Step 5: Commit**

```bash
cd /Users/dim-gggl/~/Dev\ Tools/Fancy_Tools/.worktrees/readme-generator
git add super_pocket/readme/generator.py tests/unit_tests/test_readme/test_generator.py
git commit -m "feat(readme): add core README generator

- Orchestrate section generation
- Include baseline sections (title, prereqs, install, structure)
- Support optional sections (tests, etc)
- Integrate badge generation

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 7: Basic CLI Commands

**Files:**
- Modify: `super_pocket/cli.py` (add readme group)
- Create: `super_pocket/readme/cli.py`
- Create: `tests/unit_tests/test_readme/test_cli.py`

**Step 1: Write the failing test for CLI**

Create `tests/unit_tests/test_readme/test_cli.py`:

```python
"""Tests for README CLI commands."""

import pytest
from click.testing import CliRunner
from src.super_pocket.readme.cli import readme_cli


def test_readme_cli_help():
    """Test readme CLI help message."""
    runner = CliRunner()
    result = runner.invoke(readme_cli, ["--help"])

    assert result.exit_code == 0
    assert "readme" in result.output.lower()


def test_readme_analyze_command(tmp_path):
    """Test readme analyze command."""
    # Create a Python project
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("""[project]
name = "test-project"
version = "1.0.0"
requires-python = ">=3.11"
""")

    runner = CliRunner()
    result = runner.invoke(readme_cli, ["analyze", str(tmp_path)])

    assert result.exit_code == 0
    assert "python" in result.output.lower()


def test_readme_analyze_no_project(tmp_path):
    """Test analyze command on non-project directory."""
    runner = CliRunner()
    result = runner.invoke(readme_cli, ["analyze", str(tmp_path)])

    assert result.exit_code != 0
    assert "not detect" in result.output.lower() or "no project" in result.output.lower()
```

**Step 2: Run test to verify it fails**

Run: `cd /Users/dim-gggl/~/Dev\ Tools/Fancy_Tools/.worktrees/readme-generator && source .venv/bin/activate && pytest tests/unit_tests/test_readme/test_cli.py -v`

Expected: FAIL with "No module named 'super_pocket.readme.cli'"

**Step 3: Write minimal implementation**

Create `super_pocket/readme/cli.py`:

```python
"""CLI commands for README generator."""

import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from .detector import ProjectDetector
from .generator import ReadmeGenerator

console = Console()


@click.group()
def readme_cli():
    """README generator commands."""
    pass


@readme_cli.command("analyze")
@click.argument("path", type=click.Path(exists=True), default=".")
def analyze_command(path: str):
    """
    Analyze a project and show detection results.

    Args:
        path: Project directory path (default: current directory)
    """
    project_path = Path(path).resolve()

    detector = ProjectDetector()
    context = detector.detect(project_path)

    if context is None:
        console.print("[red]Could not detect project type.[/red]")
        console.print("No recognized project files found (pyproject.toml, package.json, etc.)")
        raise click.Abort()

    # Display detection results
    table = Table(title="Project Analysis")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Project Name", context.project_name)
    table.add_row("Language", context.language.title())
    table.add_row("Project Type", context.project_type.value.replace("_", " ").title())

    if context.framework:
        table.add_row("Framework", context.framework)
    if context.runtime_version:
        table.add_row("Runtime Version", context.runtime_version)
    if context.package_manager:
        table.add_row("Package Manager", context.package_manager)

    console.print(table)

    if context.dependencies:
        console.print(f"\n[cyan]Dependencies:[/cyan] {len(context.dependencies)} found")


@readme_cli.command("generate")
@click.option("--output", "-o", default="README.md", help="Output file path")
@click.option("--path", "-p", type=click.Path(exists=True), default=".", help="Project directory")
def generate_command(output: str, path: str):
    """
    Generate a README file for the project.

    Args:
        output: Output file path
        path: Project directory path
    """
    project_path = Path(path).resolve()
    output_path = Path(output)

    # Detect project
    detector = ProjectDetector()
    context = detector.detect(project_path)

    if context is None:
        console.print("[red]Could not detect project type.[/red]")
        raise click.Abort()

    console.print(f"[cyan]Detected:[/cyan] {context.language.title()} {context.project_type.value}")

    # Generate README (minimal for now - no interactivity yet)
    generator = ReadmeGenerator()
    content = generator.generate(context, selected_badges=[], selected_sections=[])

    # Write to file
    output_path.write_text(content)
    console.print(f"[green]✓[/green] README generated: {output_path}")


if __name__ == "__main__":
    readme_cli()
```

**Step 4: Modify main CLI to include readme group**

Add to `super_pocket/cli.py` (find the cli group and add):

```python
from src.super_pocket.readme.cli import readme_cli

# Add this line inside the cli() function or after cli.add_command() calls:
cli.add_command(readme_cli, name="readme")
```

**Step 5: Run test to verify it passes**

Run: `cd /Users/dim-gggl/~/Dev\ Tools/Fancy_Tools/.worktrees/readme-generator && source .venv/bin/activate && pytest tests/unit_tests/test_readme/test_cli.py -v`

Expected: PASS (3 tests)

**Step 6: Test CLI manually**

Run: `cd /Users/dim-gggl/~/Dev\ Tools/Fancy_Tools/.worktrees/readme-generator && source .venv/bin/activate && pocket readme --help`

Expected: Shows readme commands

**Step 7: Commit**

```bash
cd /Users/dim-gggl/~/Dev\ Tools/Fancy_Tools/.worktrees/readme-generator
git add super_pocket/readme/cli.py super_pocket/cli.py tests/unit_tests/test_readme/test_cli.py
git commit -m "feat(readme): add basic CLI commands

- Add 'pocket readme analyze' to show detection results
- Add 'pocket readme generate' for basic README generation
- Integrate with main pocket CLI
- Add CLI tests

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 8: Run Full Test Suite

**Files:**
- None (verification only)

**Step 1: Run all README tests**

Run: `cd /Users/dim-gggl/~/Dev\ Tools/Fancy_Tools/.worktrees/readme-generator && source .venv/bin/activate && pytest tests/unit_tests/test_readme/ -v`

Expected: All tests PASS

**Step 2: Run entire test suite**

Run: `cd /Users/dim-gggl/~/Dev\ Tools/Fancy_Tools/.worktrees/readme-generator && source .venv/bin/activate && pytest tests/unit_tests/ -v`

Expected: 79+ tests PASS (2 pre-existing failures in web/favicon OK)

**Step 3: Test CLI in real project**

Run:
```bash
cd /Users/dim-gggl/~/Dev\ Tools/Fancy_Tools/.worktrees/readme-generator
source .venv/bin/activate
pocket readme analyze .
```

Expected: Shows analysis of super-pocket project

**Step 4: Generate sample README**

Run:
```bash
cd /Users/dim-gggl/~/Dev\ Tools/Fancy_Tools/.worktrees/readme-generator
source .venv/bin/activate
pocket readme generate -o /tmp/TEST_README.md
cat /tmp/TEST_README.md
```

Expected: Valid README generated

---

## Task 9: Update Documentation

**Files:**
- Modify: `README.md`
- Create: `docs/readme-generator.md`

**Step 1: Add feature to main README**

In `README.md`, add to Features section:

```markdown
- **README Generator**: Smart README generation with project detection and templates
```

Add to Commands Reference:

```markdown
### README Generator

```bash
# Analyze project to see what would be detected
pocket readme analyze

# Generate a README for current project
pocket readme generate

# Generate with custom output path
pocket readme generate -o docs/README.md
```

**Step 2: Create feature documentation**

Create `docs/readme-generator.md`:

```markdown
# README Generator

Smart README generation with automatic project detection.

## Features

- **Smart Detection**: Automatically detects language, framework, and project type
- **Template-Based**: Generates sections appropriate for your project type
- **Minimal but Accurate**: Focuses on essential "clone → run → contribute" content

## Quick Start

```bash
# Analyze your project
pocket readme analyze

# Generate README
pocket readme generate
```

## Current Support

### Languages
- Python (pyproject.toml detection)

### Project Types
- CLI Tools
- Web Applications
- Libraries

## Roadmap

- Interactive section selection
- Badge customization
- Multiple language support (JavaScript, Go, Rust)
- Template system with learning
- Preview and edit UI
```

**Step 3: Commit documentation**

```bash
cd /Users/dim-gggl/~/Dev\ Tools/Fancy_Tools/.worktrees/readme-generator
git add README.md docs/readme-generator.md
git commit -m "docs: add README generator documentation

- Update main README with new feature
- Add detailed feature documentation
- Include quick start and roadmap

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Summary

**MVP Implementation Complete!**

The MVP includes:
- ✅ Smart detection (Python projects)
- ✅ Project type classification (CLI/Web/Library)
- ✅ Badge generation
- ✅ Baseline sections (title, prereqs, install, structure)
- ✅ CLI commands (analyze, generate)
- ✅ Comprehensive tests
- ✅ Documentation

**What's working:**
- Detect Python projects from pyproject.toml
- Generate minimal but accurate READMEs
- CLI integration with Super Pocket

**What's next (Phase 2):**
- Interactive badge/section selection
- Template manager with learning
- Preview and edit UI
- Multiple language analyzers (JS, Go, Rust)
- Optional sections (tests, contributing, etc.)
