"""
Pytest configuration and shared fixtures.
"""

import pytest
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image

SAMPLE_ICON_SIZE = 128
SAMPLE_ICON_FILL = (12, 140, 210, 255)


@pytest.fixture
def temp_dir():
    """
    Provide a temporary directory for tests.

    Yields:
        Path: Path to temporary directory.
    """
    with TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_markdown_content():
    """
    Provide sample markdown content for testing.

    Returns:
        str: Sample markdown content.
    """
    return """# Test Document

This is a **test** document with some *markdown* formatting.

## Code Example

```python
def hello():
    print("Hello, world!")
```

## List

- Item 1
- Item 2
- Item 3
"""


@pytest.fixture
def sample_markdown_file(temp_dir, sample_markdown_content):
    """
    Create a temporary markdown file for testing.

    Args:
        temp_dir: Temporary directory fixture.
        sample_markdown_content: Sample markdown content fixture.

    Returns:
        Path: Path to the temporary markdown file.
    """
    file_path = temp_dir / "test.md"
    file_path.write_text(sample_markdown_content, encoding='utf-8')
    return file_path


@pytest.fixture
def sample_project_structure(temp_dir):
    """
    Create a sample project structure for testing.

    Args:
        temp_dir: Temporary directory fixture.

    Returns:
        Path: Path to the temporary project directory.
    """
    project_dir = temp_dir / "test_project"
    project_dir.mkdir()

    # Create some files and directories
    (project_dir / "src").mkdir()
    (project_dir / "src" / "main.py").write_text("print('Hello')", encoding='utf-8')
    (project_dir / "src" / "utils.py").write_text("def helper(): pass", encoding='utf-8')

    (project_dir / "tests").mkdir()
    (project_dir / "tests" / "test_main.py").write_text("def test_main(): pass", encoding='utf-8')

    (project_dir / "README.md").write_text("# Test Project", encoding='utf-8')

    return project_dir


@pytest.fixture
def sample_rgba_icon_file(temp_dir):
    """
    Create a valid RGBA PNG file for icon-related tests.

    Args:
        temp_dir: Temporary directory fixture.

    Returns:
        Path: Path to a PNG image fixture.
    """
    file_path = temp_dir / "sample-icon.png"
    image = Image.new("RGBA", (SAMPLE_ICON_SIZE, SAMPLE_ICON_SIZE), SAMPLE_ICON_FILL)
    image.save(file_path, format="PNG")
    return file_path
