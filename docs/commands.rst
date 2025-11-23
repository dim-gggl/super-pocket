Commands Reference
==================

Complete reference for all Super Pocket CLI commands.

Global Options
--------------

These options are available for all commands:

.. code-block:: bash

   pocket [OPTIONS] COMMAND [ARGS]...

Options:

* ``--version`` - Show version and exit
* ``--help`` - Show help message and exit

Markdown Commands
-----------------

Tools for rendering and working with Markdown files.

pocket markdown render
~~~~~~~~~~~~~~~~~~~~~~

Render a Markdown file in the terminal with beautiful formatting.

**Usage:**

.. code-block:: bash

   pocket markdown render [OPTIONS] FILE

**Arguments:**

* ``FILE`` - Path to the Markdown file to render (required)

**Options:**

* ``--help`` - Show help message

**Examples:**

.. code-block:: bash

   # Render README file
   pocket markdown render README.md

   # Render any markdown file
   pocket markdown render docs/guide.md

**Standalone Command:**

.. code-block:: bash

   markd README.md

Project Commands
----------------

Tools for exporting and managing project files.

pocket project to-file
~~~~~~~~~~~~~~~~~~~~~~

Export an entire project directory to a single Markdown file.

**Usage:**

.. code-block:: bash

   pocket project to-file [OPTIONS]

**Options:**

* ``-p, --path TEXT`` - Project directory path (default: current directory)
* ``-o, --output TEXT`` - Output file name (default: <project_name>-1-file.md)
* ``-e, --exclude TEXT`` - Comma-separated list of files/directories to exclude
* ``--help`` - Show help message

**Examples:**

.. code-block:: bash

   # Export current directory
   pocket project to-file

   # Export specific project
   pocket project to-file -p /path/to/project

   # Custom output file
   pocket project to-file -o my-export.md

   # Exclude directories
   pocket project to-file -e "node_modules,dist,venv"

   # Exclude multiple patterns
   pocket project to-file -e ".git,*.pyc,__pycache__"

**Output Format:**

The generated file includes:

* Project name and metadata
* Directory structure tree
* File contents with syntax highlighting
* Proper section headers

**Standalone Command:**

.. code-block:: bash

   proj2md -p . -o output.md

pocket project readme
~~~~~~~~~~~~~~~~~~~~~

Generate a complete ``README.md`` interactively from the inspected project.

**Usage:**

.. code-block:: bash

   pocket project readme [OPTIONS]

**Options:**

* ``-p, --path TEXT`` - Project directory to analyze (default: current directory)
* ``-o, --output TEXT`` - Path to the README file to create (default: <path>/README.md)
* ``--help`` - Show help message

**Examples:**

.. code-block:: bash

   # Generate README in current project
   pocket project readme

   # Scan another repo and save in docs/README.md
   pocket project readme -p ../demo -o docs/README.md

**What it does:**

* Detects project metadata (languages, frameworks, dependencies)
* Prompts for highlights, roadmap, usage samples, etc.
* Writes a ready-to-edit README with consistent sections

pocket project req-to-date
~~~~~~~~~~~~~~~~~~~~~~~~~~

Audit dependencies and compare installed versions with the latest releases.

**Usage:**

.. code-block:: bash

   pocket project req-to-date [PACKAGES...]

**Arguments:**

* ``PACKAGES`` - Accepts any mix of:

  - Requirement strings (``package==version``)
  - Comma-separated lists (``package_a,package_b>=2``)
  - Paths to ``requirements.txt`` or ``pyproject.toml``

**Examples:**

.. code-block:: bash

   # Check a single package
   pocket project req-to-date click==8.1.7

   # Provide a requirements file
   pocket project req-to-date requirements.txt

   # Mix multiple sources
   pocket project req-to-date numpy==1.23,rich>=13 pyproject.toml

**Output Format:**

Each dependency is printed as ``current -> latest`` with color-coded hints.
Errors on malformed inputs raise a descriptive ``BadParameter`` message.

**Standalone Command:**

.. code-block:: bash

   req-update requirements.txt

Templates Commands
------------------

Manage AI agent templates and development cheatsheets.

pocket templates list
~~~~~~~~~~~~~~~~~~~~~

List all available templates and cheatsheets.

**Usage:**

.. code-block:: bash

   pocket templates list [OPTIONS]

**Options:**

* ``-t, --type TEXT`` - Filter by type: "templates", "cheatsheets", or "all" (default: all)
* ``--help`` - Show help message

**Examples:**

.. code-block:: bash

   # List everything
   pocket templates list

   # List only templates
   pocket templates list -t templates

   # List only cheatsheets
   pocket templates list -t cheatsheets

pocket templates view
~~~~~~~~~~~~~~~~~~~~~

View the contents of a specific template or cheatsheet.

**Usage:**

.. code-block:: bash

   pocket templates view [OPTIONS] NAME

**Arguments:**

* ``NAME`` - Name of the template or cheatsheet (required)

**Options:**

* ``-t, --type TEXT`` - Type: "template" or "cheatsheet" (default: auto-detect)
* ``--help`` - Show help message

**Examples:**

.. code-block:: bash

   # View template (auto-detected)
   pocket templates view unit_tests_agent

   # View cheatsheet explicitly
   pocket templates view SQL -t cheatsheet

   # View any template
   pocket templates view agent_maker

pocket templates copy
~~~~~~~~~~~~~~~~~~~~~

Copy a template or cheatsheet to your project.

**Usage:**

.. code-block:: bash

   pocket templates copy [OPTIONS] NAME

**Arguments:**

* ``NAME`` - Name of the template or cheatsheet to copy (required)

**Options:**

* ``-o, --output TEXT`` - Output directory path (default: current directory)
* ``-t, --type TEXT`` - Type: "template" or "cheatsheet" (default: auto-detect)
* ``--help`` - Show help message

**Examples:**

.. code-block:: bash

   # Copy to current directory
   pocket templates copy unit_tests_agent

   # Copy to specific directory
   pocket templates copy unit_tests_agent -o .agents/

   # Copy cheatsheet
   pocket templates copy SQL -t cheatsheet -o ./docs/

pocket templates init
~~~~~~~~~~~~~~~~~~~~~

Initialize an agent templates directory with all available templates.

**Usage:**

.. code-block:: bash

   pocket templates init [OPTIONS]

**Options:**

* ``-o, --output TEXT`` - Output directory path (default: .agents/)
* ``--help`` - Show help message

**Examples:**

.. code-block:: bash

   # Initialize in default location (.agents/)
   pocket templates init

   # Initialize in custom location
   pocket templates init -o ./my-agents/

   # Initialize in project subdirectory
   pocket templates init -o ./config/agents/

PDF Commands
------------

Convert text and Markdown files to PDF format.

.. note::
   Requires ``super-pocket[pdf]`` optional dependencies.

pocket pdf convert
~~~~~~~~~~~~~~~~~~

Convert a text or Markdown file to PDF.

**Usage:**

.. code-block:: bash

   pocket pdf convert [OPTIONS] INPUT

**Arguments:**

* ``INPUT`` - Path to input file (required)

**Options:**

* ``-o, --output TEXT`` - Optional output PDF path (default: <input>.pdf)
* ``--help`` - Show help message

**Examples:**

.. code-block:: bash

   # Convert markdown to PDF
   pocket pdf convert document.md -o document.pdf

   # Convert text file
   pocket pdf convert notes.txt -o notes.pdf

   # Convert with custom output path
   pocket pdf convert README.md -o ~/Documents/readme.pdf

**Supported Input Formats:**

* Markdown (.md, .markdown)
* Plain text (.txt)

**Standalone Command:**

.. code-block:: bash

   conv2pdf document.md output.pdf

Web Commands
------------

Web utilities for generating favicons, querying jobs, and other assets.

.. note::
   Requires ``super-pocket[web]`` optional dependencies.

pocket web job-search
~~~~~~~~~~~~~~~~~~~~~

Scrape job listings via the `JSearch API <https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch>`_ and store them locally.

**Usage:**

.. code-block:: bash

   pocket web job-search [OPTIONS] QUERY

**Options:**

* ``-p, --page INTEGER`` - First results page (default: 1)
* ``-n, --num_pages INTEGER`` - Number of pages to traverse (default: 10)
* ``-c, --country TEXT`` - Country code (default: fr)
* ``-l, --language TEXT`` - Language code (default: fr)
* ``-d, --date_posted TEXT`` - Filter window (``today``, ``3days``, ``week``, ``month``)
* ``-t, --employment_types TEXT`` - Employment filter (e.g., ``FULLTIME``)
* ``-r, --job_requirements TEXT`` - Requirement filter (e.g., ``no_experience``)
* ``--work_from_home`` - Limit to remote-friendly positions
* ``-o, --output TEXT`` - Output JSON file (default: ``jobs.json``)
* ``--help`` - Show help message

**Environment Variables:**

* ``RAPIDAPI_API_KEY`` - Required API key for authenticated requests

**Examples:**

.. code-block:: bash

   # Fetch 5 pages of remote-friendly Python jobs in Canada
   pocket web job-search "Python developer" -c ca -l en -n 5 --work_from_home

   # Store results for later processing
   pocket web job-search "Data engineer" -o data_jobs.json

**Output Format:**

Results are saved as JSON with job metadata, company names, and job URLs.

pocket web favicon
~~~~~~~~~~~~~~~~~~

Generate a favicon from an image file.

**Usage:**

.. code-block:: bash

   pocket web favicon [OPTIONS] INPUT

**Arguments:**

* ``INPUT`` - Path to input image file (required)

**Options:**

* ``-o, --output TEXT`` - Output .ico file path (default: favicon.ico)
* ``--sizes TEXT`` - Comma-separated list of ``WIDTHxHEIGHT`` pairs (defaults to 256x256,128x128,64x64,32x32,16x16)
* ``--help`` - Show help message

**Examples:**

.. code-block:: bash

   # Generate favicon with defaults
   pocket web favicon logo.png

   # Specify output path
   pocket web favicon logo.png -o static/favicon.ico

   # Custom sizes
   pocket web favicon logo.png --sizes "48x48,32x32,16x16"

**Supported Input Formats:**

* PNG
* JPG/JPEG
* GIF
* BMP

**Standalone Command:**

.. code-block:: bash

   favicon logo.png -o favicon.ico

Command Cheat Sheet
-------------------

Quick reference table:

.. list-table::
   :widths: 30 40 30
   :header-rows: 1

   * - Command
     - Description
     - Standalone
   * - ``pocket markdown render``
     - Render markdown in terminal
     - ``markd``
   * - ``pocket project to-file``
     - Export project to file
     - ``proj2md``
   * - ``pocket project readme``
     - Generate README from project metadata
     - N/A
   * - ``pocket project req-to-date``
     - Audit dependencies and suggest upgrades
     - ``req-update``
   * - ``pocket templates list``
     - List templates/cheatsheets
     - N/A
   * - ``pocket templates view``
     - View template/cheatsheet
     - N/A
   * - ``pocket templates copy``
     - Copy template to project
     - N/A
   * - ``pocket templates init``
     - Initialize templates directory
     - N/A
   * - ``pocket pdf convert``
     - Convert to PDF
     - ``conv2pdf``
   * - ``pocket web favicon``
     - Generate favicon
     - ``favicon``
   * - ``pocket web job-search``
     - Fetch job listings from JSearch API
     - N/A

Common Patterns
---------------

Working with Multiple Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Process multiple markdown files
   for file in *.md; do
       pocket markdown render "$file"
   done

   # Export multiple projects
   for dir in projects/*/; do
       pocket project to-file -p "$dir" -o "${dir%/}-export.md"
   done

Using Output Redirection
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Save rendered output
   pocket markdown render README.md > rendered.txt

   # Export to stdout
   pocket project to-file -o - > project.md

Combining with Other Tools
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Export and search
   pocket project to-file -o - | grep "TODO"

   # Convert and view PDF
   pocket pdf convert docs.md -o docs.pdf && open docs.pdf

   # Generate favicon and verify
   pocket web favicon logo.png && file favicon.ico

Exit Codes
----------

Super Pocket commands use standard Unix exit codes:

* ``0`` - Success
* ``1`` - General error
* ``2`` - Command line usage error
* Other codes may indicate specific errors

Environment Variables
---------------------

The web job search command requires ``RAPIDAPI_API_KEY`` to be exported in your shell:

.. code-block:: bash

   export RAPIDAPI_API_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

Additional feature-specific variables may be introduced in future releases.

See Also
--------

* :doc:`quickstart` - Getting started guide
* :doc:`templates` - Templates and cheatsheets details
* :doc:`api` - API documentation
* :doc:`contributing` - Contributing to Super Pocket
