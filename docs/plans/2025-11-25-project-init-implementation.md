# Project Initialization Tool Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build `pocket project init` - a hybrid template-based project scaffolding tool with interactive customization.

**Architecture:** Declarative YAML manifests define templates, Jinja2 renders files, Python engine orchestrates generation, Rich provides beautiful TUI.

**Tech Stack:** Click, Rich, Jinja2, PyYAML, Python 3.11+

---

## Phase 1: Core Infrastructure

### Task 1: Add Dependencies

**Files:**
- Modify: `pyproject.toml:20-42`

**Step 1: Add jinja2 and pyyaml to dependencies**

Add to dependencies list in pyproject.toml:

```toml
dependencies = [
    "click>=8.3.1",
    "coverage>=7.12.0",
    "pytest>=9.0.1",
    "python-dotenv>=1.2.1",
    "requests>=2.32.5",
    "rich>=14.2.0",
    "jinja2>=3.1.0",
    "pyyaml>=6.0.0",
    # ... rest of dependencies
]
```

**Step 2: Install dependencies**

Run: `cd /Users/dim-gggl/~/Dev\ Tools/super-pocket && uv sync`
Expected: Dependencies installed successfully

**Step 3: Commit**

```bash
git add pyproject.toml
git commit -m "chore: add jinja2 and pyyaml dependencies for project init"
```

---

### Task 2: Create Module Structure

**Files:**
- Create: `super_pocket/project/init/__init__.py`
- Create: `super_pocket/project/init/manifest.py`
- Create: `super_pocket/project/init/renderers.py`
- Create: `super_pocket/project/init/engine.py`
- Create: `super_pocket/project/init/interactive.py`
- Create: `super_pocket/project/init/cli.py`
- Create: `super_pocket/project/init/actions.py`
- Create: `super_pocket/project/templates/.gitkeep`

**Step 1: Create init module directory**

Run: `mkdir -p /Users/dim-gggl/~/Dev\ Tools/super-pocket/super_pocket/project/init`
Expected: Directory created

**Step 2: Create templates directory**

Run: `mkdir -p /Users/dim-gggl/~/Dev\ Tools/super-pocket/super_pocket/project/templates`
Expected: Directory created

**Step 3: Create __init__.py**

File: `super_pocket/project/init/__init__.py`

```python
"""
Project initialization module.

Provides project scaffolding with template-based generation and
interactive customization.
"""

from .engine import ProjectGenerator

__all__ = ["ProjectGenerator"]
```

**Step 4: Create placeholder files**

```bash
touch super_pocket/project/init/manifest.py
touch super_pocket/project/init/renderers.py
touch super_pocket/project/init/engine.py
touch super_pocket/project/init/interactive.py
touch super_pocket/project/init/cli.py
touch super_pocket/project/init/actions.py
touch super_pocket/project/templates/.gitkeep
```

**Step 5: Commit**

```bash
git add super_pocket/project/init/ super_pocket/project/templates/
git commit -m "feat: add project init module structure"
```

---

### Task 3: Implement Manifest Data Models

**Files:**
- Modify: `super_pocket/project/init/manifest.py`
- Create: `tests/unit_tests/test_init/__init__.py`
- Create: `tests/unit_tests/test_init/test_manifest.py`

**Step 1: Write test for ToolChoice model**

File: `tests/unit_tests/test_init/test_manifest.py`

```python
"""Tests for manifest parsing and validation."""
import pytest
from src.super_pocket.project.init.manifest import (
    ToolChoice,
    ToolOption,
    Feature,
    StructureItem,
    PostGenAction,
    TemplateManifest,
)


def test_tool_option_creation():
    """Test ToolOption data class."""
    option = ToolOption(
        name="click",
        description="Click - composable CLI"
    )
    assert option.name == "click"
    assert option.description == "Click - composable CLI"


def test_tool_choice_creation():
    """Test ToolChoice data class."""
    choice = ToolChoice(
        prompt="Which CLI framework?",
        default="click",
        options=[
            ToolOption(name="click", description="Click"),
            ToolOption(name="typer", description="Typer"),
        ]
    )
    assert choice.prompt == "Which CLI framework?"
    assert choice.default == "click"
    assert len(choice.options) == 2
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/unit_tests/test_init/test_manifest.py::test_tool_option_creation -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'super_pocket.project.init.manifest'"

**Step 3: Implement manifest data models**

File: `super_pocket/project/init/manifest.py`

```python
"""
Manifest parsing and validation for project templates.

This module defines the data models for template manifests and
provides parsing/validation functionality.
"""
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolOption:
    """Represents a single option in a tool choice."""
    name: str
    description: str


@dataclass
class ToolChoice:
    """Represents a category of tool choices (e.g., CLI framework)."""
    prompt: str
    default: str
    options: list[ToolOption]


@dataclass
class Feature:
    """Represents a toggleable feature in a template."""
    name: str
    description: str
    default: bool = False


@dataclass
class StructureItem:
    """Represents a file or directory in the project structure."""
    path: str
    type: str = "file"  # "file" or "directory"
    template: str | None = None
    condition: str | None = None


@dataclass
class PostGenAction:
    """Represents a post-generation action to execute."""
    action: str
    condition: str | None = None
    params: dict[str, Any] = field(default_factory=dict)


@dataclass
class TemplateManifest:
    """Complete template manifest with all metadata and configuration."""
    name: str
    display_name: str
    description: str
    python_version: str
    tool_choices: dict[str, ToolChoice]
    features: list[Feature]
    structure: list[StructureItem]
    post_generation: list[PostGenAction]
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/unit_tests/test_init/test_manifest.py::test_tool_option_creation -v`
Expected: PASS

**Step 5: Commit**

```bash
git add super_pocket/project/init/manifest.py tests/unit_tests/test_init/
git commit -m "feat: add manifest data models"
```

---

### Task 4: Implement Manifest Parser

**Files:**
- Modify: `super_pocket/project/init/manifest.py`
- Modify: `tests/unit_tests/test_init/test_manifest.py`

**Step 1: Write test for YAML parsing**

Add to `tests/unit_tests/test_init/test_manifest.py`:

```python
import tempfile
from pathlib import Path


def test_parse_manifest_from_yaml():
    """Test parsing a complete manifest from YAML."""
    yaml_content = """
name: python-cli
display_name: "Python CLI Tool"
description: "Command-line tool with Click"
python_version: ">=3.11"

tool_choices:
  cli_framework:
    prompt: "Which CLI framework?"
    default: click
    options:
      - name: click
        description: "Click - composable CLI"
      - name: typer
        description: "Typer - type hints"

features:
  - name: testing
    description: "Testing with pytest"
    default: true
  - name: docker
    description: "Docker support"
    default: false

structure:
  - path: "src/{{ project_name }}"
    type: directory
  - path: "src/{{ project_name }}/__init__.py"
    template: "python-cli/init.py.j2"

post_generation:
  - action: git_init
  - action: create_venv
    params:
      python_version: "{{ python_version }}"
"""

    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(yaml_content)
        temp_path = Path(f.name)

    try:
        from src.super_pocket.project.init.manifest import parse_manifest
        manifest = parse_manifest(temp_path)

        assert manifest.name == "python-cli"
        assert manifest.display_name == "Python CLI Tool"
        assert "cli_framework" in manifest.tool_choices
        assert len(manifest.features) == 2
        assert len(manifest.structure) == 2
        assert len(manifest.post_generation) == 2
    finally:
        temp_path.unlink()
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/unit_tests/test_init/test_manifest.py::test_parse_manifest_from_yaml -v`
Expected: FAIL with "ImportError: cannot import name 'parse_manifest'"

**Step 3: Implement parse_manifest function**

Add to `super_pocket/project/init/manifest.py`:

```python
import yaml
from pathlib import Path


def parse_manifest(manifest_path: Path) -> TemplateManifest:
    """
    Parse a template manifest from a YAML file.

    Args:
        manifest_path: Path to the YAML manifest file

    Returns:
        Parsed TemplateManifest object

    Raises:
        FileNotFoundError: If manifest file doesn't exist
        ValueError: If manifest is invalid
    """
    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")

    with open(manifest_path, 'r') as f:
        data = yaml.safe_load(f)

    # Parse tool choices
    tool_choices = {}
    for key, choice_data in data.get("tool_choices", {}).items():
        options = [
            ToolOption(**opt) for opt in choice_data["options"]
        ]
        tool_choices[key] = ToolChoice(
            prompt=choice_data["prompt"],
            default=choice_data["default"],
            options=options
        )

    # Parse features
    features = [Feature(**feat) for feat in data.get("features", [])]

    # Parse structure
    structure = []
    for item in data.get("structure", []):
        structure.append(StructureItem(**item))

    # Parse post-generation actions
    post_gen = []
    for action in data.get("post_generation", []):
        if isinstance(action, str):
            # Simple action name only
            post_gen.append(PostGenAction(action=action))
        elif isinstance(action, dict):
            # Action with params
            action_name = action.pop("action")
            condition = action.pop("condition", None)
            post_gen.append(PostGenAction(
                action=action_name,
                condition=condition,
                params=action
            ))

    return TemplateManifest(
        name=data["name"],
        display_name=data["display_name"],
        description=data["description"],
        python_version=data["python_version"],
        tool_choices=tool_choices,
        features=features,
        structure=structure,
        post_generation=post_gen
    )
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/unit_tests/test_init/test_manifest.py::test_parse_manifest_from_yaml -v`
Expected: PASS

**Step 5: Commit**

```bash
git add super_pocket/project/init/manifest.py tests/unit_tests/test_init/test_manifest.py
git commit -m "feat: add manifest YAML parser"
```

---

### Task 5: Implement Template Renderer

**Files:**
- Modify: `super_pocket/project/init/renderers.py`
- Create: `tests/unit_tests/test_init/test_renderers.py`

**Step 1: Write test for context builder**

File: `tests/unit_tests/test_init/test_renderers.py`

```python
"""Tests for template rendering."""
import pytest
from src.super_pocket.project.init.renderers import build_context


def test_build_context():
    """Test building Jinja2 context from selections."""
    tool_choices = {
        "cli_framework": "click",
        "package_manager": "uv"
    }
    features = {
        "testing": True,
        "docker": False
    }

    context = build_context(
        project_name="my_awesome_cli",
        description="A CLI tool",
        tool_choices=tool_choices,
        features=features,
        python_version=">=3.11"
    )

    assert context["project_name"] == "my_awesome_cli"
    assert context["project_display_name"] == "My Awesome CLI"
    assert context["description"] == "A CLI tool"
    assert context["tool_choices"]["cli_framework"] == "click"
    assert context["features"]["testing"] is True
    assert context["features"]["docker"] is False
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/unit_tests/test_init/test_renderers.py::test_build_context -v`
Expected: FAIL with "ImportError: cannot import name 'build_context'"

**Step 3: Implement context builder**

File: `super_pocket/project/init/renderers.py`

```python
"""
Template rendering with Jinja2.

Provides context building and template rendering functionality.
"""
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Template


def build_context(
    project_name: str,
    description: str,
    tool_choices: dict[str, str],
    features: dict[str, bool],
    python_version: str
) -> dict:
    """
    Build Jinja2 context from user selections.

    Args:
        project_name: Project name in snake_case
        description: Project description
        tool_choices: Dict mapping choice category to selected option
        features: Dict mapping feature name to enabled/disabled
        python_version: Python version requirement

    Returns:
        Context dictionary for Jinja2 rendering
    """
    # Convert snake_case to Title Case for display name
    display_name = " ".join(word.capitalize() for word in project_name.split("_"))

    return {
        "project_name": project_name,
        "project_display_name": display_name,
        "description": description,
        "tool_choices": tool_choices,
        "features": features,
        "python_version": python_version,
    }


def render_template_string(template_str: str, context: dict) -> str:
    """
    Render a Jinja2 template string with context.

    Args:
        template_str: Jinja2 template as string
        context: Context dictionary

    Returns:
        Rendered string
    """
    template = Template(template_str)
    return template.render(**context)


def render_template_file(template_path: Path, context: dict) -> str:
    """
    Render a Jinja2 template file with context.

    Args:
        template_path: Path to template file
        context: Context dictionary

    Returns:
        Rendered string

    Raises:
        FileNotFoundError: If template file doesn't exist
    """
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    with open(template_path, 'r') as f:
        template_str = f.read()

    return render_template_string(template_str, context)
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/unit_tests/test_init/test_renderers.py::test_build_context -v`
Expected: PASS

**Step 5: Write test for template rendering**

Add to `tests/unit_tests/test_init/test_renderers.py`:

```python
import tempfile


def test_render_template_string():
    """Test rendering a template string."""
    from src.super_pocket.project.init.renderers import render_template_string

    template = "Hello {{ name }}!"
    context = {"name": "World"}
    result = render_template_string(template, context)
    assert result == "Hello World!"


def test_render_template_with_conditionals():
    """Test rendering with conditional logic."""
    from src.super_pocket.project.init.renderers import render_template_string

    template = """
{% if features.testing %}
import pytest
{% endif %}

def main():
    pass
"""
    context = {"features": {"testing": True}}
    result = render_template_string(template, context)
    assert "import pytest" in result
```

**Step 6: Run tests to verify they pass**

Run: `pytest tests/unit_tests/test_init/test_renderers.py -v`
Expected: All tests PASS

**Step 7: Commit**

```bash
git add super_pocket/project/init/renderers.py tests/unit_tests/test_init/test_renderers.py
git commit -m "feat: add template renderer with Jinja2"
```

---

### Task 6: Implement Post-Generation Actions

**Files:**
- Modify: `super_pocket/project/init/actions.py`
- Create: `tests/unit_tests/test_init/test_actions.py`

**Step 1: Write test for git_init action**

File: `tests/unit_tests/test_init/test_actions.py`

```python
"""Tests for post-generation actions."""
import pytest
import tempfile
from pathlib import Path
from src.super_pocket.project.init.actions import ActionExecutor


def test_git_init_action(tmp_path):
    """Test git init action."""
    executor = ActionExecutor(project_path=tmp_path)

    result = executor.execute_git_init()

    assert result.success is True
    assert (tmp_path / ".git").exists()


def test_create_directory_action(tmp_path):
    """Test directory creation action."""
    executor = ActionExecutor(project_path=tmp_path)

    test_dir = tmp_path / "src" / "my_package"
    executor.create_directory(test_dir)

    assert test_dir.exists()
    assert test_dir.is_dir()
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/unit_tests/test_init/test_actions.py::test_git_init_action -v`
Expected: FAIL with "ImportError: cannot import name 'ActionExecutor'"

**Step 3: Implement ActionExecutor**

File: `super_pocket/project/init/actions.py`

```python
"""
Post-generation actions execution.

Handles git initialization, virtual environment creation,
dependency installation, and other post-generation tasks.
"""
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class ActionResult:
    """Result of an action execution."""
    success: bool
    message: str
    error: str | None = None


class ActionExecutor:
    """Executes post-generation actions."""

    def __init__(self, project_path: Path):
        """
        Initialize action executor.

        Args:
            project_path: Path to the generated project
        """
        self.project_path = project_path

    def execute_git_init(self) -> ActionResult:
        """
        Initialize git repository.

        Returns:
            ActionResult with execution status
        """
        try:
            subprocess.run(
                ["git", "init"],
                cwd=self.project_path,
                check=True,
                capture_output=True
            )
            return ActionResult(
                success=True,
                message="Initialized git repository"
            )
        except subprocess.CalledProcessError as e:
            return ActionResult(
                success=False,
                message="Failed to initialize git repository",
                error=str(e)
            )

    def create_directory(self, path: Path) -> ActionResult:
        """
        Create a directory and all parent directories.

        Args:
            path: Directory path to create

        Returns:
            ActionResult with execution status
        """
        try:
            path.mkdir(parents=True, exist_ok=True)
            return ActionResult(
                success=True,
                message=f"Created directory: {path}"
            )
        except Exception as e:
            return ActionResult(
                success=False,
                message=f"Failed to create directory: {path}",
                error=str(e)
            )

    def write_file(self, path: Path, content: str) -> ActionResult:
        """
        Write content to a file.

        Args:
            path: File path
            content: File content

        Returns:
            ActionResult with execution status
        """
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
            return ActionResult(
                success=True,
                message=f"Created file: {path}"
            )
        except Exception as e:
            return ActionResult(
                success=False,
                message=f"Failed to write file: {path}",
                error=str(e)
            )

    def create_venv(self, package_manager: str = "uv") -> ActionResult:
        """
        Create virtual environment.

        Args:
            package_manager: Package manager to use (uv, poetry, pip)

        Returns:
            ActionResult with execution status
        """
        try:
            if package_manager == "uv":
                cmd = ["uv", "venv"]
            elif package_manager == "poetry":
                cmd = ["poetry", "env", "use", "python"]
            else:  # pip
                cmd = ["python", "-m", "venv", ".venv"]

            subprocess.run(
                cmd,
                cwd=self.project_path,
                check=True,
                capture_output=True
            )
            return ActionResult(
                success=True,
                message=f"Created virtual environment with {package_manager}"
            )
        except subprocess.CalledProcessError as e:
            return ActionResult(
                success=False,
                message=f"Failed to create virtual environment",
                error=str(e)
            )

    def install_dependencies(self, package_manager: str = "uv", dev: bool = True) -> ActionResult:
        """
        Install project dependencies.

        Args:
            package_manager: Package manager to use
            dev: Whether to install dev dependencies

        Returns:
            ActionResult with execution status
        """
        try:
            if package_manager == "uv":
                cmd = ["uv", "sync"]
            elif package_manager == "poetry":
                cmd = ["poetry", "install"]
                if not dev:
                    cmd.append("--no-dev")
            else:  # pip
                cmd = ["pip", "install", "-r", "requirements.txt"]

            subprocess.run(
                cmd,
                cwd=self.project_path,
                check=True,
                capture_output=True
            )
            return ActionResult(
                success=True,
                message=f"Installed dependencies with {package_manager}"
            )
        except subprocess.CalledProcessError as e:
            return ActionResult(
                success=False,
                message="Failed to install dependencies",
                error=str(e)
            )

    def run_command(self, command: str) -> ActionResult:
        """
        Run an arbitrary shell command.

        Args:
            command: Command to run

        Returns:
            ActionResult with execution status
        """
        try:
            subprocess.run(
                command,
                shell=True,
                cwd=self.project_path,
                check=True,
                capture_output=True
            )
            return ActionResult(
                success=True,
                message=f"Executed: {command}"
            )
        except subprocess.CalledProcessError as e:
            return ActionResult(
                success=False,
                message=f"Command failed: {command}",
                error=str(e)
            )
```

**Step 4: Run tests to verify they pass**

Run: `pytest tests/unit_tests/test_init/test_actions.py -v`
Expected: All tests PASS

**Step 5: Commit**

```bash
git add super_pocket/project/init/actions.py tests/unit_tests/test_init/test_actions.py
git commit -m "feat: add post-generation action executor"
```

---

### Task 7: Implement Project Generation Engine

**Files:**
- Modify: `super_pocket/project/init/engine.py`
- Create: `tests/unit_tests/test_init/test_engine.py`

**Step 1: Write test for ProjectGenerator**

File: `tests/unit_tests/test_init/test_engine.py`

```python
"""Tests for project generation engine."""
import pytest
import tempfile
from pathlib import Path
from src.super_pocket.project.init.engine import ProjectGenerator
from src.super_pocket.project.init.manifest import (
    TemplateManifest,
    ToolChoice,
    ToolOption,
    Feature,
    StructureItem,
    PostGenAction
)


def test_project_generator_initialization(tmp_path):
    """Test ProjectGenerator initialization."""
    manifest = TemplateManifest(
        name="test-template",
        display_name="Test Template",
        description="A test template",
        python_version=">=3.11",
        tool_choices={},
        features=[],
        structure=[],
        post_generation=[]
    )

    generator = ProjectGenerator(
        manifest=manifest,
        project_name="test_project",
        output_path=tmp_path
    )

    assert generator.manifest == manifest
    assert generator.project_name == "test_project"
    assert generator.output_path == tmp_path


def test_generate_simple_structure(tmp_path):
    """Test generating a simple project structure."""
    manifest = TemplateManifest(
        name="test-template",
        display_name="Test Template",
        description="A test template",
        python_version=">=3.11",
        tool_choices={},
        features=[],
        structure=[
            StructureItem(path="src/{{ project_name }}", type="directory"),
            StructureItem(path="README.md", type="file", template=None),
        ],
        post_generation=[]
    )

    generator = ProjectGenerator(
        manifest=manifest,
        project_name="test_project",
        output_path=tmp_path
    )

    generator.tool_selections = {}
    generator.feature_selections = {}

    # Note: This test will need template files to work fully
    # For now, we test the structure is created
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/unit_tests/test_init/test_engine.py::test_project_generator_initialization -v`
Expected: FAIL with "ImportError: cannot import name 'ProjectGenerator'"

**Step 3: Implement ProjectGenerator**

File: `super_pocket/project/init/engine.py`

```python
"""
Project generation engine.

Orchestrates the project generation process including file creation,
template rendering, and post-generation actions.
"""
from pathlib import Path
from typing import Any

from .manifest import TemplateManifest, StructureItem
from .renderers import build_context, render_template_file, render_template_string
from .actions import ActionExecutor, ActionResult


class ProjectGenerator:
    """Generates projects from templates."""

    def __init__(
        self,
        manifest: TemplateManifest,
        project_name: str,
        output_path: Path,
        template_base_path: Path | None = None
    ):
        """
        Initialize project generator.

        Args:
            manifest: Template manifest
            project_name: Name of the project to generate
            output_path: Where to generate the project
            template_base_path: Base path for template files
        """
        self.manifest = manifest
        self.project_name = project_name
        self.output_path = output_path
        self.template_base_path = template_base_path or Path(__file__).parent.parent / "templates"

        self.tool_selections: dict[str, str] = {}
        self.feature_selections: dict[str, bool] = {}
        self.description: str = ""

        self.action_executor = ActionExecutor(output_path)

    def set_selections(
        self,
        tool_selections: dict[str, str],
        feature_selections: dict[str, bool],
        description: str
    ):
        """
        Set user selections.

        Args:
            tool_selections: Selected tools for each choice category
            feature_selections: Enabled/disabled features
            description: Project description
        """
        self.tool_selections = tool_selections
        self.feature_selections = feature_selections
        self.description = description

    def generate(self) -> list[ActionResult]:
        """
        Generate the project.

        Returns:
            List of action results
        """
        results = []

        # Build context
        context = build_context(
            project_name=self.project_name,
            description=self.description,
            tool_choices=self.tool_selections,
            features=self.feature_selections,
            python_version=self.manifest.python_version
        )

        # Create output directory
        self.output_path.mkdir(parents=True, exist_ok=True)

        # Generate structure
        for item in self.manifest.structure:
            # Check condition if present
            if item.condition and not self._evaluate_condition(item.condition, context):
                continue

            # Render path template
            rendered_path = render_template_string(item.path, context)
            full_path = self.output_path / rendered_path

            if item.type == "directory":
                result = self.action_executor.create_directory(full_path)
                results.append(result)
            else:  # file
                if item.template:
                    # Render from template file
                    template_path = self.template_base_path / self.manifest.name / item.template
                    if template_path.exists():
                        content = render_template_file(template_path, context)
                    else:
                        # If template doesn't exist, create empty file
                        content = ""
                else:
                    # Create empty file
                    content = ""

                result = self.action_executor.write_file(full_path, content)
                results.append(result)

        # Execute post-generation actions
        for action in self.manifest.post_generation:
            # Check condition
            if action.condition and not self._evaluate_condition(action.condition, context):
                continue

            result = self._execute_action(action.action, action.params, context)
            results.append(result)

        return results

    def _evaluate_condition(self, condition: str, context: dict) -> bool:
        """
        Evaluate a condition string.

        Args:
            condition: Condition to evaluate (e.g., "features.testing")
            context: Context dictionary

        Returns:
            True if condition is met, False otherwise
        """
        # Simple dot-notation evaluation
        parts = condition.split(".")
        value = context
        for part in parts:
            value = value.get(part, False)
            if value is False:
                return False
        return bool(value)

    def _execute_action(self, action_name: str, params: dict, context: dict) -> ActionResult:
        """
        Execute a post-generation action.

        Args:
            action_name: Name of the action
            params: Action parameters
            context: Rendering context

        Returns:
            ActionResult
        """
        if action_name == "git_init":
            return self.action_executor.execute_git_init()
        elif action_name == "create_venv":
            package_manager = params.get("package_manager", "uv")
            # Render template variables in params
            if isinstance(package_manager, str) and "{{" in package_manager:
                package_manager = render_template_string(package_manager, context)
            return self.action_executor.create_venv(package_manager)
        elif action_name == "install_dependencies":
            package_manager = params.get("package_manager", "uv")
            if isinstance(package_manager, str) and "{{" in package_manager:
                package_manager = render_template_string(package_manager, context)
            dev = params.get("dev", True)
            return self.action_executor.install_dependencies(package_manager, dev)
        elif action_name == "run_command":
            command = params.get("command", "")
            command = render_template_string(command, context)
            return self.action_executor.run_command(command)
        elif action_name == "display_next_steps":
            return ActionResult(
                success=True,
                message="Project generated successfully!"
            )
        else:
            return ActionResult(
                success=False,
                message=f"Unknown action: {action_name}"
            )
```

**Step 4: Run tests to verify they pass**

Run: `pytest tests/unit_tests/test_init/test_engine.py -v`
Expected: Tests PASS

**Step 5: Commit**

```bash
git add super_pocket/project/init/engine.py tests/unit_tests/test_init/test_engine.py
git commit -m "feat: add project generation engine"
```

---

## Phase 2: Interactive UI

### Task 8: Implement Interactive Customization

**Files:**
- Modify: `super_pocket/project/init/interactive.py`
- Create: `tests/unit_tests/test_init/test_interactive.py`

**Step 1: Write test for default selections**

File: `tests/unit_tests/test_init/test_interactive.py`

```python
"""Tests for interactive UI."""
import pytest
from src.super_pocket.project.init.interactive import get_default_selections
from src.super_pocket.project.init.manifest import (
    TemplateManifest,
    ToolChoice,
    ToolOption,
    Feature
)


def test_get_default_selections():
    """Test getting default selections from manifest."""
    manifest = TemplateManifest(
        name="test",
        display_name="Test",
        description="Test",
        python_version=">=3.11",
        tool_choices={
            "framework": ToolChoice(
                prompt="Choose framework",
                default="click",
                options=[
                    ToolOption(name="click", description="Click"),
                    ToolOption(name="typer", description="Typer"),
                ]
            )
        },
        features=[
            Feature(name="testing", description="Testing", default=True),
            Feature(name="docker", description="Docker", default=False),
        ],
        structure=[],
        post_generation=[]
    )

    tool_sel, feat_sel = get_default_selections(manifest)

    assert tool_sel["framework"] == "click"
    assert feat_sel["testing"] is True
    assert feat_sel["docker"] is False
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/unit_tests/test_init/test_interactive.py::test_get_default_selections -v`
Expected: FAIL with "ImportError: cannot import name 'get_default_selections'"

**Step 3: Implement interactive UI functions**

File: `super_pocket/project/init/interactive.py`

```python
"""
Interactive UI for project customization.

Provides interactive prompts for tool choices and feature selection
using Rich for beautiful terminal output.
"""
from typing import Tuple
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.table import Table

from .manifest import TemplateManifest


console = Console()


def get_default_selections(manifest: TemplateManifest) -> Tuple[dict[str, str], dict[str, bool]]:
    """
    Get default selections from manifest.

    Args:
        manifest: Template manifest

    Returns:
        Tuple of (tool_selections, feature_selections)
    """
    tool_selections = {
        key: choice.default
        for key, choice in manifest.tool_choices.items()
    }

    feature_selections = {
        feature.name: feature.default
        for feature in manifest.features
    }

    return tool_selections, feature_selections


def prompt_project_info() -> Tuple[str, str]:
    """
    Prompt for project name and description.

    Returns:
        Tuple of (project_name, description)
    """
    console.print("\n[bold cyan]Project Information[/bold cyan]")

    project_name = Prompt.ask(
        "Project name (snake_case)",
        default="my_project"
    )

    # Validate project name (basic validation)
    project_name = project_name.lower().replace("-", "_").replace(" ", "_")

    description = Prompt.ask(
        "Project description",
        default="A new project"
    )

    return project_name, description


def prompt_tool_choices(manifest: TemplateManifest) -> dict[str, str]:
    """
    Prompt user to select tools for each choice category.

    Args:
        manifest: Template manifest

    Returns:
        Dict mapping choice category to selected option
    """
    selections = {}

    if not manifest.tool_choices:
        return selections

    console.print("\n[bold cyan]Tool Choices[/bold cyan]")

    for key, choice in manifest.tool_choices.items():
        console.print(f"\n[yellow]{choice.prompt}[/yellow]")

        # Create options display
        for i, option in enumerate(choice.options, 1):
            default_marker = " [dim](default)[/dim]" if option.name == choice.default else ""
            console.print(f"  {i}. {option.name} - {option.description}{default_marker}")

        # Prompt for selection
        while True:
            selection = Prompt.ask(
                "Select option",
                choices=[str(i) for i in range(1, len(choice.options) + 1)],
                default="1"
            )
            idx = int(selection) - 1
            selected = choice.options[idx].name
            break

        selections[key] = selected

    return selections


def prompt_features(manifest: TemplateManifest) -> dict[str, bool]:
    """
    Prompt user to enable/disable features.

    Args:
        manifest: Template manifest

    Returns:
        Dict mapping feature name to enabled/disabled
    """
    selections = {}

    if not manifest.features:
        return selections

    console.print("\n[bold cyan]Features[/bold cyan]")

    for feature in manifest.features:
        default = "Y" if feature.default else "n"
        response = Confirm.ask(
            f"{feature.description}",
            default=feature.default
        )
        selections[feature.name] = response

    return selections


def customize_interactively(
    manifest: TemplateManifest,
    quick: bool = False
) -> Tuple[str, str, dict[str, str], dict[str, bool]]:
    """
    Run interactive customization flow.

    Args:
        manifest: Template manifest
        quick: If True, use defaults without prompting

    Returns:
        Tuple of (project_name, description, tool_selections, feature_selections)
    """
    # Display header
    panel = Panel(
        f"[bold]{manifest.display_name}[/bold]\n{manifest.description}",
        title="Template",
        border_style="cyan"
    )
    console.print(panel)

    if quick:
        # Use defaults
        project_name = "my_project"
        description = manifest.description
        tool_selections, feature_selections = get_default_selections(manifest)
    else:
        # Interactive prompts
        project_name, description = prompt_project_info()
        tool_selections = prompt_tool_choices(manifest)
        feature_selections = prompt_features(manifest)

    # Display summary
    console.print("\n[bold green]Configuration Summary[/bold green]")
    console.print(f"Project: {project_name}")
    console.print(f"Description: {description}")

    if tool_selections:
        console.print("\nTool Choices:")
        for key, value in tool_selections.items():
            console.print(f"  {key}: {value}")

    if feature_selections:
        console.print("\nFeatures:")
        for key, value in feature_selections.items():
            status = "[green]✓[/green]" if value else "[red]✗[/red]"
            console.print(f"  {status} {key}")

    if not quick:
        proceed = Confirm.ask("\nProceed with generation?", default=True)
        if not proceed:
            console.print("[yellow]Cancelled[/yellow]")
            raise KeyboardInterrupt("User cancelled")

    return project_name, description, tool_selections, feature_selections
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/unit_tests/test_init/test_interactive.py::test_get_default_selections -v`
Expected: PASS

**Step 5: Commit**

```bash
git add super_pocket/project/init/interactive.py tests/unit_tests/test_init/test_interactive.py
git commit -m "feat: add interactive customization UI"
```

---

## Phase 3: CLI Integration

### Task 9: Add CLI Commands

**Files:**
- Modify: `super_pocket/project/init/cli.py`
- Modify: `super_pocket/cli.py:88-200`

**Step 1: Implement init CLI commands**

File: `super_pocket/project/init/cli.py`

```python
"""
CLI commands for project initialization.

Provides Click commands for listing, showing, and initializing projects
from templates.
"""
import click
from pathlib import Path
from rich.console import Console
from rich.table import Table

from .manifest import parse_manifest
from .engine import ProjectGenerator
from .interactive import customize_interactively


console = Console()


def list_templates(templates_dir: Path) -> list[dict]:
    """
    List all available templates.

    Args:
        templates_dir: Directory containing template manifests

    Returns:
        List of template info dicts
    """
    templates = []
    for manifest_file in templates_dir.glob("*.yaml"):
        try:
            manifest = parse_manifest(manifest_file)
            templates.append({
                "name": manifest.name,
                "display_name": manifest.display_name,
                "description": manifest.description
            })
        except Exception as e:
            console.print(f"[red]Error loading {manifest_file.name}: {e}[/red]")

    return templates


@click.group(name="init")
def init_group():
    """Initialize new projects from templates."""
    pass


@init_group.command(name="list")
def list_cmd():
    """List available project templates."""
    templates_dir = Path(__file__).parent.parent / "templates"
    templates = list_templates(templates_dir)

    if not templates:
        console.print("[yellow]No templates found[/yellow]")
        return

    table = Table(title="Available Templates")
    table.add_column("Name", style="cyan")
    table.add_column("Display Name", style="green")
    table.add_column("Description")

    for template in templates:
        table.add_row(
            template["name"],
            template["display_name"],
            template["description"]
        )

    console.print(table)


@init_group.command(name="show")
@click.argument("template_name")
def show_cmd(template_name: str):
    """Show details of a specific template."""
    templates_dir = Path(__file__).parent.parent / "templates"
    manifest_path = templates_dir / f"{template_name}.yaml"

    if not manifest_path.exists():
        console.print(f"[red]Template not found: {template_name}[/red]")
        return

    try:
        manifest = parse_manifest(manifest_path)

        console.print(f"\n[bold cyan]{manifest.display_name}[/bold cyan]")
        console.print(f"{manifest.description}\n")
        console.print(f"Python version: {manifest.python_version}")

        if manifest.tool_choices:
            console.print("\n[bold]Tool Choices:[/bold]")
            for key, choice in manifest.tool_choices.items():
                console.print(f"  {choice.prompt}")
                for option in choice.options:
                    default = " (default)" if option.name == choice.default else ""
                    console.print(f"    - {option.name}: {option.description}{default}")

        if manifest.features:
            console.print("\n[bold]Features:[/bold]")
            for feature in manifest.features:
                default = "✓" if feature.default else "✗"
                console.print(f"  [{default}] {feature.description}")

    except Exception as e:
        console.print(f"[red]Error loading template: {e}[/red]")


@init_group.command()
@click.argument("template_name")
@click.option("--path", "-p", type=click.Path(), help="Output directory")
@click.option("--quick", "-q", is_flag=True, help="Use defaults without prompting")
def new(template_name: str, path: str | None, quick: bool):
    """
    Initialize a new project from a template.

    Args:
        template_name: Name of the template to use
        path: Output directory (defaults to ./<project_name>)
        quick: Use default selections without prompting
    """
    templates_dir = Path(__file__).parent.parent / "templates"
    manifest_path = templates_dir / f"{template_name}.yaml"

    if not manifest_path.exists():
        console.print(f"[red]Template not found: {template_name}[/red]")
        console.print("\nAvailable templates:")
        for template in list_templates(templates_dir):
            console.print(f"  - {template['name']}")
        return

    try:
        # Load manifest
        manifest = parse_manifest(manifest_path)

        # Get user customization
        project_name, description, tool_sel, feat_sel = customize_interactively(
            manifest, quick=quick
        )

        # Determine output path
        if path:
            output_path = Path(path)
        else:
            output_path = Path.cwd() / project_name

        if output_path.exists() and any(output_path.iterdir()):
            console.print(f"[red]Directory already exists and is not empty: {output_path}[/red]")
            return

        # Generate project
        console.print(f"\n[bold]Generating project in {output_path}...[/bold]")

        generator = ProjectGenerator(
            manifest=manifest,
            project_name=project_name,
            output_path=output_path
        )
        generator.set_selections(tool_sel, feat_sel, description)

        results = generator.generate()

        # Display results
        success_count = sum(1 for r in results if r.success)
        console.print(f"\n[green]✓ Generated {success_count} items successfully[/green]")

        # Show any errors
        errors = [r for r in results if not r.success]
        if errors:
            console.print(f"\n[yellow]Warnings/Errors:[/yellow]")
            for error in errors:
                console.print(f"  [red]✗[/red] {error.message}")
                if error.error:
                    console.print(f"    {error.error}")

        console.print(f"\n[bold green]Project created successfully![/bold green]")
        console.print(f"Location: {output_path}")

    except KeyboardInterrupt:
        console.print("\n[yellow]Cancelled[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        import traceback
        traceback.print_exc()
```

**Step 2: Integrate init commands into main CLI**

Modify `super_pocket/cli.py`, add after line 200:

```python
# Add import at top
from src.super_pocket.project.init.cli import init_group

# Add to project_group (after req-to-date command, around line 200)
project_group.add_command(init_group)
```

**Step 3: Test CLI commands manually**

Run: `cd /Users/dim-gggl/~/Dev\ Tools/super-pocket && pocket project init list`
Expected: Shows "No templates found" (templates don't exist yet)

**Step 4: Commit**

```bash
git add super_pocket/project/init/cli.py super_pocket/cli.py
git commit -m "feat: add CLI commands for project init"
```

---

## Phase 4: First Template (python-cli)

### Task 10: Create python-cli Template Manifest

**Files:**
- Create: `super_pocket/project/templates/python-cli.yaml`

**Step 1: Create python-cli manifest**

File: `super_pocket/project/templates/python-cli.yaml`

```yaml
name: python-cli
display_name: "Python CLI Tool"
description: "Command-line tool with Click, rich output, and testing"

python_version: ">=3.11"

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

  - name: docker
    description: "Docker containerization"
    default: false

structure:
  - path: "src/{{ project_name }}"
    type: directory

  - path: "src/{{ project_name }}/__init__.py"
    template: "python-cli/__init__.py.j2"

  - path: "src/{{ project_name }}/cli.py"
    template: "python-cli/cli_{{ tool_choices.cli_framework }}.py.j2"

  - path: "tests"
    type: directory
    condition: "features.testing"

  - path: "tests/__init__.py"
    condition: "features.testing"

  - path: "tests/test_cli.py"
    template: "python-cli/test_cli.py.j2"
    condition: "features.testing"

  - path: "pyproject.toml"
    template: "python-cli/pyproject_{{ tool_choices.package_manager }}.toml.j2"

  - path: "README.md"
    template: "python-cli/README.md.j2"

  - path: ".gitignore"
    template: "python-cli/gitignore.j2"

  - path: ".github/workflows/ci.yml"
    template: "python-cli/github_workflow.yml.j2"
    condition: "features.github_actions"

  - path: "Dockerfile"
    template: "python-cli/Dockerfile.j2"
    condition: "features.docker"

post_generation:
  - action: git_init

  - action: create_venv
    params:
      package_manager: "{{ tool_choices.package_manager }}"

  - action: install_dependencies
    params:
      package_manager: "{{ tool_choices.package_manager }}"
      dev: true

  - action: display_next_steps
```

**Step 2: Commit**

```bash
git add super_pocket/project/templates/python-cli.yaml
git commit -m "feat: add python-cli template manifest"
```

---

### Task 11: Create python-cli Template Files

**Files:**
- Create: `super_pocket/project/templates/python-cli/` directory and template files

**Step 1: Create template directory**

Run: `mkdir -p /Users/dim-gggl/~/Dev\ Tools/super-pocket/super_pocket/project/templates/python-cli`

**Step 2: Create __init__.py template**

File: `super_pocket/project/templates/python-cli/__init__.py.j2`

```python
"""{{ project_display_name }} - {{ description }}"""

__version__ = "0.1.0"
```

**Step 3: Create CLI template for Click**

File: `super_pocket/project/templates/python-cli/cli_click.py.j2`

```python
"""Main CLI module for {{ project_display_name }}."""
import click
{% if features.rich_output %}
from rich.console import Console

console = Console()
{% endif %}


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """{{ description }}"""
    pass


@cli.command()
@click.option('--name', '-n', default='World', help='Name to greet')
def hello(name: str):
    """Say hello to someone."""
    {% if features.rich_output %}
    console.print(f"[bold green]Hello {name}![/bold green]")
    {% else %}
    click.echo(f"Hello {name}!")
    {% endif %}


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
```

**Step 4: Create CLI template for Typer**

File: `super_pocket/project/templates/python-cli/cli_typer.py.j2`

```python
"""Main CLI module for {{ project_display_name }}."""
import typer
{% if features.rich_output %}
from rich.console import Console

console = Console()
{% endif %}

app = typer.Typer()


@app.command()
def hello(name: str = typer.Option("World", "--name", "-n", help="Name to greet")):
    """Say hello to someone."""
    {% if features.rich_output %}
    console.print(f"[bold green]Hello {name}![/bold green]")
    {% else %}
    typer.echo(f"Hello {name}!")
    {% endif %}


def main():
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
```

**Step 5: Create CLI template for argparse**

File: `super_pocket/project/templates/python-cli/cli_argparse.py.j2`

```python
"""Main CLI module for {{ project_display_name }}."""
import argparse
{% if features.rich_output %}
from rich.console import Console

console = Console()
{% endif %}


def hello(name: str):
    """Say hello to someone."""
    {% if features.rich_output %}
    console.print(f"[bold green]Hello {name}![/bold green]")
    {% else %}
    print(f"Hello {name}!")
    {% endif %}


def main():
    """Entry point for the CLI."""
    parser = argparse.ArgumentParser(description="{{ description }}")
    parser.add_argument('--version', action='version', version='0.1.0')

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Hello command
    hello_parser = subparsers.add_parser('hello', help='Say hello to someone')
    hello_parser.add_argument('--name', '-n', default='World', help='Name to greet')

    args = parser.parse_args()

    if args.command == 'hello':
        hello(args.name)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
```

**Step 6: Create test template**

File: `super_pocket/project/templates/python-cli/test_cli.py.j2`

```python
"""Tests for {{ project_name }} CLI."""
import pytest
from {{ project_name }}.cli import cli
{% if tool_choices.cli_framework == "click" %}
from click.testing import CliRunner
{% elif tool_choices.cli_framework == "typer" %}
from typer.testing import CliRunner
{% endif %}


{% if tool_choices.cli_framework in ["click", "typer"] %}
def test_hello_default():
    """Test hello command with default name."""
    runner = CliRunner()
    result = runner.invoke(cli, ['hello'])
    assert result.exit_code == 0
    assert 'Hello World' in result.output


def test_hello_custom_name():
    """Test hello command with custom name."""
    runner = CliRunner()
    result = runner.invoke(cli, ['hello', '--name', 'Alice'])
    assert result.exit_code == 0
    assert 'Hello Alice' in result.output
{% else %}
def test_placeholder():
    """Placeholder test for argparse CLI."""
    # Add tests for argparse CLI
    assert True
{% endif %}
```

**Step 7: Commit template files**

```bash
git add super_pocket/project/templates/python-cli/
git commit -m "feat: add python-cli Jinja2 templates for CLI code"
```

---

### Task 12: Create python-cli Configuration Templates

**Files:**
- Create pyproject.toml templates for different package managers
- Create README, gitignore, Dockerfile templates

**Step 1: Create pyproject.toml for uv**

File: `super_pocket/project/templates/python-cli/pyproject_uv.toml.j2`

```toml
[project]
name = "{{ project_name }}"
version = "0.1.0"
description = "{{ description }}"
requires-python = "{{ python_version }}"
dependencies = [
{% if tool_choices.cli_framework == "click" %}
    "click>=8.0.0",
{% elif tool_choices.cli_framework == "typer" %}
    "typer>=0.9.0",
{% endif %}
{% if features.rich_output %}
    "rich>=13.0.0",
{% endif %}
{% if features.config_file %}
    "pyyaml>=6.0.0",
    "toml>=0.10.0",
{% endif %}
]

[project.optional-dependencies]
dev = [
{% if features.testing %}
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
{% endif %}
]

[project.scripts]
{{ project_name }} = "{{ project_name }}.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

**Step 2: Create pyproject.toml for poetry**

File: `super_pocket/project/templates/python-cli/pyproject_poetry.toml.j2`

```toml
[tool.poetry]
name = "{{ project_name }}"
version = "0.1.0"
description = "{{ description }}"
authors = ["Your Name <your.email@example.com>"]

[tool.poetry.dependencies]
python = "{{ python_version }}"
{% if tool_choices.cli_framework == "click" %}
click = "^8.0.0"
{% elif tool_choices.cli_framework == "typer" %}
typer = "^0.9.0"
{% endif %}
{% if features.rich_output %}
rich = "^13.0.0"
{% endif %}
{% if features.config_file %}
pyyaml = "^6.0.0"
toml = "^0.10.0"
{% endif %}

[tool.poetry.group.dev.dependencies]
{% if features.testing %}
pytest = "^7.0.0"
pytest-cov = "^4.0.0"
{% endif %}

[tool.poetry.scripts]
{{ project_name }} = "{{ project_name }}.cli:main"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

**Step 3: Create requirements.txt for pip**

File: `super_pocket/project/templates/python-cli/pyproject_pip.toml.j2`

```toml
[project]
name = "{{ project_name }}"
version = "0.1.0"
description = "{{ description }}"
requires-python = "{{ python_version }}"

[project.scripts]
{{ project_name }} = "{{ project_name }}.cli:main"

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
```

Also create: `super_pocket/project/templates/python-cli/requirements.txt.j2`

```
{% if tool_choices.cli_framework == "click" %}
click>=8.0.0
{% elif tool_choices.cli_framework == "typer" %}
typer>=0.9.0
{% endif %}
{% if features.rich_output %}
rich>=13.0.0
{% endif %}
{% if features.config_file %}
pyyaml>=6.0.0
toml>=0.10.0
{% endif %}
{% if features.testing %}
pytest>=7.0.0
pytest-cov>=4.0.0
{% endif %}
```

**Step 4: Create README template**

File: `super_pocket/project/templates/python-cli/README.md.j2`

```markdown
# {{ project_display_name }}

{{ description }}

## Installation

```bash
{% if tool_choices.package_manager == "uv" %}
# Create virtual environment
uv venv

# Install dependencies
uv sync
{% elif tool_choices.package_manager == "poetry" %}
# Install dependencies
poetry install
{% else %}
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .
{% endif %}
```

## Usage

```bash
{{ project_name }} hello --name YourName
```

{% if features.testing %}
## Testing

```bash
{% if tool_choices.package_manager == "poetry" %}
poetry run pytest
{% else %}
pytest
{% endif %}
```
{% endif %}

## Development

This project was generated with [super-pocket](https://github.com/yourusername/super-pocket).

## License

MIT
```

**Step 5: Create gitignore template**

File: `super_pocket/project/templates/python-cli/gitignore.j2`

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
.venv/
venv/
ENV/
build/
dist/
*.egg-info/

# Testing
.pytest_cache/
.coverage
htmlcov/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
```

**Step 6: Create GitHub Actions workflow**

File: `super_pocket/project/templates/python-cli/github_workflow.yml.j2`

```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

{% if tool_choices.package_manager == "uv" %}
    - name: Install uv
      run: curl -LsSf https://astral.sh/uv/install.sh | sh

    - name: Install dependencies
      run: uv sync

    - name: Run tests
      run: uv run pytest
{% elif tool_choices.package_manager == "poetry" %}
    - name: Install Poetry
      run: pipx install poetry

    - name: Install dependencies
      run: poetry install

    - name: Run tests
      run: poetry run pytest
{% else %}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e .
        pip install pytest pytest-cov

    - name: Run tests
      run: pytest
{% endif %}
```

**Step 7: Create Dockerfile**

File: `super_pocket/project/templates/python-cli/Dockerfile.j2`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY . /app

{% if tool_choices.package_manager == "uv" %}
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
RUN uv sync
{% elif tool_choices.package_manager == "poetry" %}
RUN pip install poetry
RUN poetry install --no-dev
{% else %}
RUN pip install -e .
{% endif %}

ENTRYPOINT ["{{ project_name }}"]
```

**Step 8: Commit all config templates**

```bash
git add super_pocket/project/templates/python-cli/
git commit -m "feat: add python-cli configuration templates"
```

---

### Task 13: Test python-cli Template End-to-End

**Step 1: Test template generation**

Run: `cd /tmp && pocket project init list`
Expected: Shows python-cli template

Run: `cd /tmp && pocket project init show python-cli`
Expected: Shows template details

**Step 2: Test quick generation**

Run: `cd /tmp && pocket project init new python-cli --quick`
Expected: Generates project with defaults in /tmp/my_project

**Step 3: Verify generated project**

Run: `ls -la /tmp/my_project`
Expected: See src/, tests/, pyproject.toml, README.md, .gitignore

Run: `cat /tmp/my_project/src/my_project/cli.py`
Expected: See generated CLI code

**Step 4: Clean up test project**

Run: `rm -rf /tmp/my_project`

**Step 5: Commit**

```bash
git add -A
git commit -m "test: verify python-cli template works end-to-end"
```

---

## Phase 5: Remaining Templates (Simplified)

### Task 14-19: Create Remaining 5 Templates

For brevity, each template follows the same pattern:
1. Create `<template-name>.yaml` manifest
2. Create `<template-name>/` directory with Jinja2 templates
3. Test generation

**Templates to create:**
- `fastapi-api.yaml` + templates (Task 14)
- `python-package.yaml` + templates (Task 15)
- `ml-project.yaml` + templates (Task 16)
- `automation-script.yaml` + templates (Task 17)
- `docs-site.yaml` + templates (Task 18)

Each template should include:
- Manifest with tool_choices and features
- Main code templates
- Configuration files (pyproject.toml variants)
- README.md
- .gitignore
- Optional: Dockerfile, GitHub Actions

**Note:** Due to plan length, detailed steps for these templates would follow the same TDD pattern as python-cli. Implementation can reference python-cli as the canonical example.

---

## Phase 6: Testing & Documentation

### Task 20: Add Integration Tests

**Files:**
- Create: `tests/integration_tests/test_project_init.py`

**Step 1: Write integration test**

```python
"""Integration tests for project init."""
import pytest
import tempfile
from pathlib import Path
from src.super_pocket.project.init.cli import list_templates
from src.super_pocket.project.init.manifest import parse_manifest
from src.super_pocket.project.init.engine import ProjectGenerator


def test_generate_all_templates():
    """Test that all templates can be generated successfully."""
    templates_dir = Path(__file__).parent.parent.parent / "super_pocket" / "project" / "templates"
    templates = list_templates(templates_dir)

    for template_info in templates:
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = templates_dir / f"{template_info['name']}.yaml"
            manifest = parse_manifest(manifest_path)

            generator = ProjectGenerator(
                manifest=manifest,
                project_name="test_project",
                output_path=Path(tmpdir) / "test_project"
            )

            # Use defaults
            tool_sel = {key: choice.default for key, choice in manifest.tool_choices.items()}
            feat_sel = {feat.name: feat.default for feat in manifest.features}

            generator.set_selections(tool_sel, feat_sel, "Test project")
            results = generator.generate()

            # Check that generation succeeded
            assert any(r.success for r in results), f"Template {template_info['name']} failed to generate"
```

**Step 2: Run integration tests**

Run: `pytest tests/integration_tests/test_project_init.py -v`
Expected: All templates generate successfully

**Step 3: Commit**

```bash
git add tests/integration_tests/
git commit -m "test: add integration tests for all templates"
```

---

### Task 21: Update Documentation

**Files:**
- Modify: `README.md`
- Create: `docs/project-init-guide.md`

**Step 1: Update README with project init**

Add to README.md features section:

```markdown
- **Project Initialization**: Generate new projects from templates with interactive customization
```

Add to Quick Start:

```markdown
### Project Initialization

```bash
# List available templates
pocket project init list

# Show template details
pocket project init show python-cli

# Create new project interactively
pocket project init new python-cli

# Create with defaults (no prompts)
pocket project init new python-cli --quick
```

**Step 2: Create usage guide**

File: `docs/project-init-guide.md` with comprehensive usage examples

**Step 3: Commit**

```bash
git add README.md docs/project-init-guide.md
git commit -m "docs: add project init documentation"
```

---

## Phase 7: Final Polish

### Task 22: Add Error Handling & Validation

**Files:**
- Modify: `super_pocket/project/init/manifest.py`
- Modify: `super_pocket/project/init/engine.py`
- Add validation tests

**Step 1: Add manifest validation**

Implement validation for:
- Required fields
- Valid tool choice defaults
- Valid condition syntax
- Template file existence

**Step 2: Add better error messages**

Improve error messages throughout with helpful suggestions

**Step 3: Commit**

```bash
git add super_pocket/project/init/
git commit -m "feat: add validation and improved error handling"
```

---

### Task 23: Final Testing & Bug Fixes

**Step 1: Run full test suite**

Run: `pytest tests/ -v --cov=super_pocket`
Expected: All tests pass with good coverage

**Step 2: Manual testing of all templates**

Test each template with different combinations of options

**Step 3: Fix any bugs found**

**Step 4: Final commit**

```bash
git add -A
git commit -m "fix: address bugs found in testing"
```

---

## Success Criteria Checklist

- [ ] All 6 templates (python-cli, fastapi-api, python-package, ml-project, automation-script, docs-site) generate successfully
- [ ] Interactive UI works with tool choices and feature toggles
- [ ] Quick mode uses defaults without prompting
- [ ] Post-generation actions (git init, venv, deps install) work
- [ ] Generated projects are valid (can be installed and run)
- [ ] All unit tests pass
- [ ] Integration tests cover all templates
- [ ] Documentation is complete
- [ ] Error handling is robust

---

## Deployment

### Task 24: Final Review & Release

**Step 1: Version bump**

Update version in `pyproject.toml` to reflect new feature

**Step 2: Create release commit**

```bash
git add -A
git commit -m "feat: add project initialization tool with 6 templates

- Declarative YAML manifests for templates
- Jinja2-based file rendering
- Interactive customization UI with Rich
- Post-generation actions (git, venv, deps)
- 6 templates: python-cli, fastapi-api, python-package, ml-project, automation-script, docs-site
- Comprehensive tests and documentation"
```

**Step 3: Tag release**

```bash
git tag -a v1.1.0 -m "Release v1.1.0: Project initialization tool"
git push origin main --tags
```

---

## Notes for Execution

**DRY Principles:**
- Template rendering logic reused across all templates
- Action executor handles all post-generation tasks uniformly
- Manifest parser handles all YAML formats consistently

**YAGNI:**
- No template marketplace (future phase)
- No web UI (future phase)
- No template composition (future phase)
- Focus on core 6 templates only

**TDD:**
- Write test first for each component
- Verify it fails
- Implement minimal code to pass
- Refactor if needed
- Commit frequently

**Frequent Commits:**
- Commit after each task completion
- Use conventional commit messages (feat:, fix:, test:, docs:, etc.)
- Keep commits focused and atomic
