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
