Installation
============

Pick the install path that matches your workflow; all routes are quick.

Requirements
------------

* Python 3.11 or higher
* pip, uv, or Homebrew
* Virtual environment (recommended so your globals stay clean)

Installation Methods
--------------------

Using Homebrew (macOS/Linux) — Recommended
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The easiest way to install Super Pocket on macOS or Linux:

.. code-block:: bash

   brew tap dim-gggl/super-pocket
   brew install super-pocket

This installs Super Pocket system-wide without needing to manage Python environments.

Using pip (Standard)
~~~~~~~~~~~~~~~~~~~~

The simplest way to install Super Pocket is using pip:

.. code-block:: bash

   pip install super-pocket

To install with optional dependencies:

.. code-block:: bash

   # Install with PDF support
   pip install "super-pocket[pdf]"

   # Install with web utilities
   pip install "super-pocket[web]"

   # Install with all optional features
   pip install "super-pocket[all]"

   # Install with development dependencies
   pip install "super-pocket[dev]"

Using uv (Recommended for Python users)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`uv <https://github.com/astral-sh/uv>`_ is a blazing-fast Python package installer and resolver:

.. code-block:: bash

   # Install uv if you haven't already
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Install Super Pocket as a tool (globally available)
   uv tool install super-pocket

   # Or install with all features
   uv tool install "super-pocket[all]"

To install in a project environment:

.. code-block:: bash

   # Install in current environment
   uv pip install super-pocket

   # Or install with all features
   uv pip install "super-pocket[all]"

From Source
~~~~~~~~~~~

To install Super Pocket from source for development:

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/dim-gggl/super-pocket.git
   cd super-pocket

   # Create and activate virtual environment
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

   # Install in editable mode
   pip install -e .

   # Or with all dependencies
   pip install -e ".[all,dev]"

Using uv for Development
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/dim-gggl/super-pocket.git
   cd super-pocket

   # Install dependencies with uv
   uv sync

   # Install in editable mode with all features
   uv pip install -e ".[all,dev]"

   # Activate virtual environment
   source .venv/bin/activate

Optional Dependencies
---------------------

Super Pocket has several optional feature sets:

PDF Features (``super-pocket[pdf]``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Required for PDF conversion functionality:

* ``fpdf2>=2.7.0`` - PDF generation library
* ``markdown-pdf>=1.0.0`` - Markdown to PDF converter

.. code-block:: bash

   pip install "super-pocket[pdf]"

Web Features (``super-pocket[web]``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Required for web utilities like favicon generation:

* ``Pillow>=10.0.0`` - Image processing library

.. code-block:: bash

   pip install "super-pocket[web]"

Development Dependencies (``super-pocket[dev]``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Required for contributing to Super Pocket:

* ``pytest>=7.0.0`` - Testing framework
* ``pytest-cov>=3.0.0`` - Coverage plugin
* ``black>=23.0.0`` - Code formatter
* ``ruff>=0.1.0`` - Fast Python linter

.. code-block:: bash

   pip install "super-pocket[dev]"

All Features (``super-pocket[all]``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install everything except development dependencies:

.. code-block:: bash

   pip install "super-pocket[all]"

Verifying Installation
----------------------

Sanity check right after install:

.. code-block:: bash

   pocket --version
   pocket --help
   pocket markdown render README.md
   echo "# Hello Super Pocket" > test.md
   pocket markdown render test.md

You should see:

.. code-block:: text

   pocket, version 1.0.1

   Usage: pocket [OPTIONS] COMMAND [ARGS]...

     Super Pocket - Developer productivity tools collection

   Options:
     --version  Show the version and exit.
     --help     Show this message and exit.

   Commands:
     markdown   Markdown rendering tools
     pdf        PDF conversion tools
     project    Project export tools
     documents  Agent templates and cheatsheets management
     web        Web utilities

Virtual Environment Setup
--------------------------

It's strongly recommended to use a virtual environment:

Using venv
~~~~~~~~~~

.. code-block:: bash

   # Create virtual environment
   python -m venv .venv

   # Activate on Linux/macOS
   source .venv/bin/activate

   # Activate on Windows
   .venv\Scripts\activate

   # Install Super Pocket
   pip install super-pocket

Using conda
~~~~~~~~~~~

.. code-block:: bash

   # Create conda environment
   conda create -n super-pocket python=3.11

   # Activate environment
   conda activate super-pocket

   # Install Super Pocket
   pip install super-pocket

Troubleshooting
---------------

Command Not Found
~~~~~~~~~~~~~~~~~

If you get a "command not found" error after installation:

1. Ensure your virtual environment is activated
2. Check that the installation directory is in your PATH
3. Try running with ``python -m pocket`` instead of ``pocket``

Permission Errors
~~~~~~~~~~~~~~~~~

If you encounter permission errors during installation:

.. code-block:: bash

   # Use --user flag
   pip install --user super-pocket

   # Or use a virtual environment (recommended)
   python -m venv .venv
   source .venv/bin/activate
   pip install super-pocket

Import Errors
~~~~~~~~~~~~~

If you get import errors when running Super Pocket:

1. Ensure you're using Python 3.11 or higher: ``python --version``
2. Reinstall with ``pip install --force-reinstall super-pocket``
3. Check for conflicting packages: ``pip list | grep super-pocket``

Optional Dependencies Missing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If PDF or web features don't work:

.. code-block:: bash

   # Install missing dependencies
   pip install "super-pocket[all]"

   # Or install specific feature set
   pip install "super-pocket[pdf]" "super-pocket[web]"

Next Steps
----------

Now that Super Pocket is installed, head over to the :doc:`quickstart` guide to learn how to use it!

See Also
--------

* :doc:`quickstart` - Quick start guide
* :doc:`commands` - Complete command reference
* :doc:`contributing` - Contributing to Super Pocket
