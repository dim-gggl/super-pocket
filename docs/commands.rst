Commands Reference
==================

Friendly, concrete tour of every Super Pocket CLI command (plus the stand-alone shortcuts when they exist).

Interactive Mode
----------------

When you run ``pocket`` without any arguments, Super Pocket launches an interactive mode with a guided menu. This is great for discovering features or when you don't remember the exact command syntax.

**Launch interactive mode:**

.. code-block:: bash

   pocket

The interactive mode offers:

* **Help** - Display the main help menu
* **Project** - Access project tools (to-file, readme, req-to-date, init)
* **Templates** - Manage templates and cheatsheets (list, view, copy, init)
* **PDF** - Convert files to PDF
* **Web** - Web utilities (favicon, job-search)
* **README** - Analyze or generate README files
* **XML** - Convert custom tag syntax to XML
* **Exit** - Quit the interactive mode (or press ``Q``, ``q``, ``exit``, ``quit``)

Each submenu guides you through the available options and prompts for required parameters. Perfect for beginners or occasional users who prefer a guided experience over memorizing CLI flags.

**Example session:**

.. code-block:: text

   $ pocket
   [Logo appears]
   help project templates pdf web readme xml exit/Q >>> project
   [Project menu]
   help to-file readme req-to-date init exit/Q >>> to-file
   Project path [.]: ./my-app
   Output file (optional): export.md
   Exclude (comma-separated, optional): node_modules,dist
   [Spinner: Exporting project...]
   [Output displayed]
   Press Enter to continue

Global Options
--------------

These options are available everywhere:

.. code-block:: bash

   pocket [OPTIONS] COMMAND [ARGS]...

* ``--version`` - Show version and exit
* ``--help`` - Show help message and exit

Markdown Commands
-----------------

Tools for rendering and working with Markdown.

pocket markdown render
~~~~~~~~~~~~~~~~~~~~~~

Render a Markdown file in the terminal with nice formatting.

**Usage:**

.. code-block:: bash

   pocket markdown render [OPTIONS] FILE

**Arguments:**

* ``FILE`` - Path to the Markdown file (required)

**Options:**

* ``-w, --width INTEGER`` - Optional output width
* ``--help`` - Show help

**Example:**

.. code-block:: bash

   pocket markdown render README.md -w 100

**Standalone command:** ``markd README.md``

Project Commands
----------------

Everything about exporting, documenting, and scaffolding projects.

pocket project to-file
~~~~~~~~~~~~~~~~~~~~~~

Export a project directory to a single Markdown file.

**Usage:** ``pocket project to-file [OPTIONS]``

Options you’ll actually use:

* ``-p, --path`` - Project root (default: ``.``)
* ``-o, --output`` - Output file (default: ``<project>-1-file.md``)
* ``-e, --exclude`` - Comma-separated exclusions

**Examples:**

.. code-block:: bash

   pocket project to-file
   pocket project to-file -p ./my-app -o export.md
   pocket project to-file -e ".git,venv,node_modules"

**Standalone command:** ``proj2md -p . -o output.md``

pocket project readme
~~~~~~~~~~~~~~~~~~~~~

Interactive wizard that inspects the repo and writes a polished ``README.md``.

**Usage:** ``pocket project readme [OPTIONS]``

* ``-p, --path`` - Project directory (default: ``.``)
* ``-o, --output`` - Target README path (default: ``README.md``)

**Example:** ``pocket project readme -p ../demo -o docs/README.md``

What it does: detects languages/frameworks, asks a few questions, and writes a push-ready README.

pocket project req-to-date
~~~~~~~~~~~~~~~~~~~~~~~~~~

Audits dependencies and prints ``current -> latest`` with colors.

**Usage:** ``pocket project req-to-date [PACKAGES...]``

Accepts inline specs, comma lists, or files (``requirements.txt`` / ``pyproject.toml``).

**Examples:**

.. code-block:: bash

   pocket project req-to-date requirements.txt
   pocket project req-to-date click==8.1.7 rich>=13
   pocket project req-to-date numpy==1.23,rich>=13 pyproject.toml

**Standalone command:** ``req-update requirements.txt``

pocket project init
~~~~~~~~~~~~~~~~~~~

Scaffold a new project from built-in templates (great for demos or quick starts).

**Usage:** ``pocket project init [COMMAND] [OPTIONS]``

Subcommands:

* ``list`` – show available templates
* ``show <template>`` – inspect one template
* ``new <template>`` – generate a project (``--quick`` to skip prompts, ``-p`` for output path)

**Examples:**

.. code-block:: bash

   pocket project init list
   pocket project init show fastapi-basic
   pocket project init new fastapi-basic --quick -p ./demo-api

README Commands
---------------

Direct access to the README engine (same core as ``pocket project readme``).

pocket readme analyze
~~~~~~~~~~~~~~~~~~~~~

Analyze a project and print what was detected.

.. code-block:: bash

   pocket readme analyze -p .

Shows project name, language, framework (if any), and dependency count in a rich table.

pocket readme generate
~~~~~~~~~~~~~~~~~~~~~~

Generate a README in one go, no Q&A.

.. code-block:: bash

   pocket readme generate -p . -o README.md

Outputs a ready-to-edit README based on the detected stack.

Templates Commands
------------------

Manage AI agent templates and cheatsheets.

pocket templates list
~~~~~~~~~~~~~~~~~~~~~

List every template/cheatsheet (filter with ``-t templates`` or ``-t cheatsheets``).

pocket templates view
~~~~~~~~~~~~~~~~~~~~~

Preview content in the terminal. Auto-detects type or specify ``-t template|cheatsheet``.

pocket templates copy
~~~~~~~~~~~~~~~~~~~~~

Copy a template/cheatsheet to your project. Supports ``-o`` for destination and ``-f`` to overwrite.

pocket templates init
~~~~~~~~~~~~~~~~~~~~~

Bootstrap a directory with all templates (default: ``.AGENTS``). Pass ``-o`` to choose another path.

PDF Commands
------------

Convert Markdown/text to PDF.

pocket pdf convert
~~~~~~~~~~~~~~~~~~

**Usage:** ``pocket pdf convert [OPTIONS] INPUT``

* ``-o, --output`` - Output PDF path (default: ``<input>.pdf``)

**Example:** ``pocket pdf convert README.md -o README.pdf``

**Standalone command:** ``conv2pdf README.md README.pdf``

Web Commands
------------

Small web helpers (requires ``super-pocket[web]`` extras).

pocket web favicon
~~~~~~~~~~~~~~~~~~

Turn an image into a multi-size ``.ico``.

.. code-block:: bash

   pocket web favicon logo.png -o favicon.ico --sizes "64x64,32x32"

**Standalone command:** ``favicon logo.png -o favicon.ico``

pocket web job-search
~~~~~~~~~~~~~~~~~~~~~

Scrape jobs via the JSearch API and save JSON.

.. code-block:: bash

   pocket web job-search "Python developer" --work_from_home -n 5 -o jobs.json

Requires ``RAPIDAPI_API_KEY`` in the environment. Supports locale filters, pagination, and employment type filters.

XML Command
-----------

Friendly XML builder for LLMs.

pocket xml
~~~~~~~~~~

Convert ``tag:<content>`` syntax to pretty XML.

.. code-block:: bash

   pocket xml "note:hello world"
   pocket xml -f input.txt -o output.xml

If no text/file is provided, it prompts interactively. No standalone alias yet—call via ``pocket xml``.

Command Cheat Sheet
-------------------

Quick reference:

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
     - Export project to one Markdown
     - ``proj2md``
   * - ``pocket project readme``
     - Interactive README wizard
     - N/A
   * - ``pocket project req-to-date``
     - Dependency audit
     - ``req-update``
   * - ``pocket project init``
     - Scaffold from templates
     - N/A
   * - ``pocket readme analyze|generate``
     - Analyze or generate README directly
     - N/A
   * - ``pocket templates list/view/copy/init``
     - Manage templates & cheatsheets
     - N/A
   * - ``pocket pdf convert``
     - Convert to PDF
     - ``conv2pdf``
   * - ``pocket web favicon``
     - Create favicons
     - ``favicon``
   * - ``pocket web job-search``
     - Fetch job listings
     - N/A
   * - ``pocket xml``
     - Friendly syntax to XML
     - N/A
