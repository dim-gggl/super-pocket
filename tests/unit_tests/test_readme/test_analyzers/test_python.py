"""Tests for Python project analyzer."""

import pytest
from pathlib import Path
from super_pocket.readme.analyzers.python import PythonAnalyzer
from super_pocket.readme.models import ProjectType


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
