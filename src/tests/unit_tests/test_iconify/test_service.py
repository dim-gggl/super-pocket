"""
Tests for icon squircle generation services.
"""

import pytest
from PIL import Image

from super_pocket.iconify.service import (
    MASK_BACKGROUND_VALUE,
    MASK_FOREGROUND_VALUE,
    generate_superellipse_mask,
    iconify_image,
)

MASK_SIZE = 9
CORNER_COORDINATE = (0, 0)
CENTER_COORDINATE = (MASK_SIZE // 2, MASK_SIZE // 2)
OUTPUT_DIRECTORY_NAME = "generated"
OUTPUT_FILE_NAME = "iconified.png"


def test_should_generate_mask_with_opaque_center_and_transparent_corner():
    """The superellipse mask should keep the center and remove the corners."""
    mask = generate_superellipse_mask(size=MASK_SIZE)

    assert mask.getpixel(CENTER_COORDINATE) == MASK_FOREGROUND_VALUE
    assert mask.getpixel(CORNER_COORDINATE) == MASK_BACKGROUND_VALUE


def test_should_raise_value_error_when_mask_size_is_not_positive():
    """Mask generation should reject non-positive sizes."""
    with pytest.raises(ValueError, match="strictly positive"):
        generate_superellipse_mask(size=0)


def test_should_create_squircle_icon_with_transparent_corners(sample_rgba_icon_file,
                                                              temp_dir):
    """Icon generation should preserve content inside the squircle and clear corners."""
    output_file = temp_dir / OUTPUT_FILE_NAME

    generated_path = iconify_image(sample_rgba_icon_file, output_file, size=MASK_SIZE)

    with Image.open(generated_path) as generated_image:
        assert generated_path == output_file.resolve()
        assert generated_image.getpixel(CENTER_COORDINATE)[3] == MASK_FOREGROUND_VALUE
        assert generated_image.getpixel(CORNER_COORDINATE)[3] == MASK_BACKGROUND_VALUE


def test_should_create_output_parent_directory_when_missing(sample_rgba_icon_file, temp_dir):
    """Icon generation should create the destination directory tree when needed."""
    output_directory = temp_dir / OUTPUT_DIRECTORY_NAME
    output_file = output_directory / OUTPUT_FILE_NAME

    iconify_image(sample_rgba_icon_file, output_file, size=MASK_SIZE)

    assert output_directory.exists()
    assert output_file.exists()


def test_should_raise_file_not_found_when_source_image_is_missing(temp_dir):
    """Icon generation should fail fast when the source image does not exist."""
    missing_source = temp_dir / "missing.png"
    output_file = temp_dir / OUTPUT_FILE_NAME

    with pytest.raises(FileNotFoundError, match=str(missing_source)):
        iconify_image(missing_source, output_file, size=MASK_SIZE)
