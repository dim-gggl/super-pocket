API Reference
=============

Friendly tour of the public modules you can import when you want to script Super Pocket instead of clicking around the CLI.

Core & CLI
----------

.. automodule:: super_pocket
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: super_pocket.cli
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: super_pocket.interactive
   :members:
   :undoc-members:
   :show-inheritance:

Markdown
--------

.. automodule:: super_pocket.markdown
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: super_pocket.markdown.renderer
   :members:
   :undoc-members:
   :show-inheritance:

Projects
--------

.. automodule:: super_pocket.project
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: super_pocket.project.to_file
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: super_pocket.project.req_to_date
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: super_pocket.project.init.cli
   :members:
   :undoc-members:
   :show-inheritance:

README Generator
----------------

.. automodule:: super_pocket.readme
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: super_pocket.readme.detector
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: super_pocket.readme.generator
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: super_pocket.readme.cli
   :members:
   :undoc-members:
   :show-inheritance:

PDF
---

.. note::
   Requires ``super-pocket[pdf]`` optional dependencies.

.. automodule:: super_pocket.pdf
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: super_pocket.pdf.converter
   :members:
   :undoc-members:
   :show-inheritance:

Web
---

.. note::
   Requires ``super-pocket[web]`` optional dependencies.

.. automodule:: super_pocket.web
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: super_pocket.web.favicon
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: super_pocket.web.job_search
   :members:
   :undoc-members:
   :show-inheritance:

Templates & Cheatsheets
-----------------------

.. automodule:: super_pocket.templates_and_cheatsheets
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: super_pocket.templates_and_cheatsheets.cli
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: super_pocket.templates_and_cheatsheets.validator
   :members:
   :undoc-members:
   :show-inheritance:

XML Helper
----------

.. automodule:: super_pocket.xml
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: super_pocket.xml.cli
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: super_pocket.xml.xml
   :members:
   :undoc-members:
   :show-inheritance:

Utilities
---------

.. automodule:: super_pocket.settings
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: super_pocket.utils
   :members:
   :undoc-members:
   :show-inheritance:

Programmatic Examples
---------------------

Render Markdown
~~~~~~~~~~~~~~~

.. code-block:: python

   from pathlib import Path
   from super_pocket.markdown.renderer import read_markdown_file, render_markdown

   content = read_markdown_file(Path("README.md"))
   render_markdown(content)  # prints to the terminal via Rich

Export a project to one file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from super_pocket.project.to_file import create_codebase_markdown

   create_codebase_markdown(
       project_path=".",
       output_file="export.md",
       exclude_str=".git,venv,node_modules"
   )

Audit dependencies
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from super_pocket.project.req_to_date import run_req_to_date

   results = run_req_to_date(("requests==2.31.0", "rich>=13"))
   for pkg in results:
       print(pkg.package, pkg.current_version, "->", pkg.latest_overall)

Generate a README programmatically
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from pathlib import Path
   from super_pocket.readme.detector import ProjectDetector
   from super_pocket.readme.generator import ReadmeGenerator

   context = ProjectDetector().detect(Path("."))
   content = ReadmeGenerator().generate(context, selected_badges=[], selected_sections=[])
   Path("README.md").write_text(content)

Convert to PDF
~~~~~~~~~~~~~~

.. code-block:: python

   from pathlib import Path
   from super_pocket.pdf.converter import convert_to_pdf

   convert_to_pdf(Path("README.md"), Path("README.pdf"))

Make a favicon
~~~~~~~~~~~~~~

.. code-block:: python

   from pathlib import Path
   from super_pocket.web.favicon import convert_to_favicon

   convert_to_favicon(
       input_file=Path("logo.png"),
       output_file=Path("favicon.ico"),
       sizes="64x64,32x32,16x16"
   )

Build XML for LLMs
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from super_pocket.xml.xml import parse_custom_syntax, format_xml

   raw = parse_custom_syntax("note:hello world")
   pretty = format_xml(raw)
   print(pretty)

Error handling is standard Python exceptions (``FileNotFoundError``, ``ValueError``, etc.). Most modules avoid fancy wrappers so you can catch and log as you like.

API Stability
-------------

Public functions/classes documented here are the intended surface area. Private helpers (prefixed with ``_``) can change without notice. Super Pocket follows semantic versioning for releases.
