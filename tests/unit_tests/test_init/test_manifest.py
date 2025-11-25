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


def test_feature_creation():
    """Test Feature data class."""
    feature = Feature(
        name="docker",
        description="Docker support",
        default=True
    )
    assert feature.name == "docker"
    assert feature.description == "Docker support"
    assert feature.default is True


def test_structure_item_creation():
    """Test StructureItem data class."""
    item = StructureItem(
        path="src/main.py",
        type="file",
        template="main.py.j2",
        condition="features.docker"
    )
    assert item.path == "src/main.py"
    assert item.type == "file"
    assert item.template == "main.py.j2"
    assert item.condition == "features.docker"


def test_post_gen_action_creation():
    """Test PostGenAction data class."""
    action = PostGenAction(
        action="run_command",
        condition="features.docker",
        params={"command": "docker build"}
    )
    assert action.action == "run_command"
    assert action.condition == "features.docker"
    assert action.params == {"command": "docker build"}


def test_template_manifest_creation():
    """Test TemplateManifest data class."""
    manifest = TemplateManifest(
        name="python-cli",
        display_name="Python CLI",
        description="A Python CLI template",
        python_version="3.11",
        tool_choices={
            "cli": ToolChoice(
                prompt="Which CLI framework?",
                default="click",
                options=[ToolOption(name="click", description="Click")]
            )
        },
        features=[Feature(name="docker", description="Docker support")],
        structure=[StructureItem(path="src/main.py")],
        post_generation=[PostGenAction(action="run_command")]
    )
    assert manifest.name == "python-cli"
    assert manifest.display_name == "Python CLI"
    assert manifest.description == "A Python CLI template"
    assert manifest.python_version == "3.11"
    assert "cli" in manifest.tool_choices
    assert len(manifest.features) == 1
    assert len(manifest.structure) == 1
    assert len(manifest.post_generation) == 1
