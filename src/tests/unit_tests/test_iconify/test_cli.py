"""
Tests for the `pocket iconify` CLI command.
"""

import pytest
from click.testing import CliRunner
from PIL import Image

from super_pocket.cli import cli

ICON_SIZE_OPTION = "32"
OUTPUT_FILE_NAME = "iconified-cli.png"
CORNER_COORDINATE = (0, 0)


@pytest.fixture
def runner():
    """Provide a CliRunner instance for iconify command tests."""
    return CliRunner()


def test_should_generate_png_when_iconify_command_is_invoked(runner: CliRunner,
                                                             sample_rgba_icon_file,
                                                             temp_dir):
    """The CLI should generate a PNG with transparent corners."""
    output_file = temp_dir / OUTPUT_FILE_NAME

    result = runner.invoke(
        cli,
        [
            "iconify",
            "-i",
            str(sample_rgba_icon_file),
            "-o",
            str(output_file),
            "--size",
            ICON_SIZE_OPTION,
        ],
    )

    assert result.exit_code == 0
    assert output_file.exists()

    with Image.open(output_file) as generated_image:
        assert generated_image.size == (int(ICON_SIZE_OPTION), int(ICON_SIZE_OPTION))
        assert generated_image.getpixel(CORNER_COORDINATE)[3] == 0


def test_should_fail_when_iconify_command_receives_missing_file(runner: CliRunner,
                                                                temp_dir):
    """The CLI should reject a non-existent source image."""
    missing_source = temp_dir / "missing.png"
    output_file = temp_dir / OUTPUT_FILE_NAME

    result = runner.invoke(
        cli,
        [
            "iconify",
            "-i",
            str(missing_source),
            "-o",
            str(output_file),
        ],
    )

    assert result.exit_code != 0
    assert "does not exist" in result.output.lower()
