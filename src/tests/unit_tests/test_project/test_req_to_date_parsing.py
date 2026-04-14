"""Unit tests for dependency-spec parsing in req_to_date."""

from pathlib import Path

import pytest

from super_pocket.project.req_to_date import _expand_spec_inputs, parse_package_specs


@pytest.fixture
def single_requirement_file(tmp_path: Path) -> Path:
    """Create a minimal requirements file with one valid pinned dependency."""
    requirements_file = tmp_path / "requirements.txt"
    requirements_file.write_text("demo==0.1.0\n", encoding="utf-8")
    return requirements_file


def test_should_read_single_line_requirements_file(single_requirement_file: Path) -> None:
    """A one-line requirements file should produce one expanded dependency spec."""
    expanded_specs = _expand_spec_inputs([str(single_requirement_file)])
    assert expanded_specs == ["demo==0.1.0"]


def test_should_raise_value_error_when_spec_has_no_pinned_version() -> None:
    """Unpinned dependency specs must raise ValueError with a clear message."""
    with pytest.raises(ValueError, match="name==version"):
        parse_package_specs(["click"])


def test_should_raise_value_error_when_input_list_is_empty() -> None:
    """Empty inputs must be rejected with a ValueError."""
    with pytest.raises(ValueError, match="cannot be empty"):
        parse_package_specs([])
