Module Index
============

Complete map of Super Pocket modules so you know where to import from.

Package Layout
--------------

.. code-block:: text

   super_pocket/
   ├── cli.py                          # Main CLI entrypoint
   ├── interactive.py                  # Interactive prompt
   ├── markdown/
   │   └── renderer.py                 # Markdown rendering
   ├── project/
   │   ├── to_file.py                  # Export project to one Markdown
   │   ├── req_to_date.py              # Dependency audit
   │   └── init/                       # Project scaffolding
   │       └── cli.py
   ├── readme/
   │   ├── detector.py                 # Project detection
   │   ├── generator.py                # README generation
   │   └── cli.py                      # Analyze/generate commands
   ├── pdf/
   │   └── converter.py                # Markdown/text to PDF
   ├── web/
   │   ├── favicon.py                  # Favicon generation
   │   └── job_search.py               # JSearch API wrapper
   ├── xml/
   │   └── xml.py                      # tag:<content> to XML
   ├── templates_and_cheatsheets/
   │   ├── cli.py
   │   ├── validator.py
   │   ├── templates/
   │   └── cheatsheets/
   ├── settings.py                     # Shared Click/Rich helpers
   └── utils.py                        # Common error/printing helpers

Core Modules
------------

.. autosummary::
   :toctree: _autosummary

   super_pocket
   super_pocket.cli
   super_pocket.interactive

Markdown Modules
----------------

.. autosummary::
   :toctree: _autosummary

   super_pocket.markdown
   super_pocket.markdown.renderer

Project Modules
---------------

.. autosummary::
   :toctree: _autosummary

   super_pocket.project
   super_pocket.project.to_file
   super_pocket.project.req_to_date
   super_pocket.project.init.cli

README Modules
--------------

.. autosummary::
   :toctree: _autosummary

   super_pocket.readme
   super_pocket.readme.detector
   super_pocket.readme.generator
   super_pocket.readme.cli

PDF Modules
-----------

.. autosummary::
   :toctree: _autosummary

   super_pocket.pdf
   super_pocket.pdf.converter

Web Modules
-----------

.. autosummary::
   :toctree: _autosummary

   super_pocket.web
   super_pocket.web.favicon
   super_pocket.web.job_search

Templates & Cheatsheets
-----------------------

.. autosummary::
   :toctree: _autosummary

   super_pocket.templates_and_cheatsheets
   super_pocket.templates_and_cheatsheets.cli
   super_pocket.templates_and_cheatsheets.validator
   super_pocket.templates_and_cheatsheets.templates
   super_pocket.templates_and_cheatsheets.cheatsheets

XML Modules
-----------

.. autosummary::
   :toctree: _autosummary

   super_pocket.xml
   super_pocket.xml.cli
   super_pocket.xml.xml

Utilities
---------

.. autosummary::
   :toctree: _autosummary

   super_pocket.settings
   super_pocket.utils

Module Dependencies
-------------------

Core
~~~~

* ``click`` - CLI framework
* ``rich`` - Terminal formatting
* ``python-dotenv`` - Env loading for interactive bits
* ``requests`` - HTTP client

Optional
~~~~~~~~

*PDF* (``super-pocket[pdf]``): ``fpdf2``, ``markdown-pdf``

*Web* (``super-pocket[web]``): ``Pillow``

*Dev* (``super-pocket[dev]``): ``pytest``, ``pytest-cov``, ``black``, ``ruff``

Import Patterns
---------------

.. code-block:: python

   from super_pocket.markdown.renderer import read_markdown_file, render_markdown
   from super_pocket.project.to_file import create_codebase_markdown
   from super_pocket.project.req_to_date import run_req_to_date
   from super_pocket.readme.generator import ReadmeGenerator
   from super_pocket.readme.detector import ProjectDetector
   from super_pocket.web.favicon import convert_to_favicon
   from super_pocket.xml.xml import parse_custom_syntax

   # Render markdown
   render_markdown(read_markdown_file("README.md"))

   # Export project
   create_codebase_markdown(".", "export.md", ".git,venv,node_modules")

   # Audit deps
   run_req_to_date(("click==8.1.7", "rich>=13"))

   # Generate README content
   ctx = ProjectDetector().detect(".")
   content = ReadmeGenerator().generate(ctx, [], [])
