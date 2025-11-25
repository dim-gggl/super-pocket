"""Tests for manifest parsing and validation."""
import pytest
from super_pocket.project.init.manifest import (
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
