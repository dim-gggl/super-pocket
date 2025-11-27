super-pocket
============

.. image:: https://img.shields.io/badge/version-1.0.1-blue.svg
   :alt: Version 1.0.1

.. image:: https://img.shields.io/badge/python-3.11+-blue.svg
   :alt: Python 3.11+

.. image:: https://img.shields.io/badge/license-MIT-green.svg
   :alt: MIT License

**super-pocket** is a friendly grab-bag of developer tools in one CLI: pretty markdown rendering, one-file project exports,
README generation, dependency checks, XML helpers, templates, cheatsheets, and more.

Features
--------

**Markdown Rendering**
   Beautiful terminal rendering of Markdown files with syntax highlighting and rich formatting

**Project Export**
   Convert entire projects to single Markdown files for easy sharing and documentation

**README Generator**
   Inspect a repo and spit out a push-ready README (interactive or one-shot)

**Agent Templates**
   Manage and distribute AI agent configuration templates for consistent AI-assisted development

**Cheatsheets**
   Quick access to development cheatsheets and reference materials

**Dependency Scanner**
   Spot outdated packages from inline specs, requirements.txt, or pyproject.toml

**PDF Tools**
   Convert markdown and text files to professional PDF documents

**Web Utilities**
   Generate favicons and other web assets from images

**LLM-Friendly XML**
   Turn ``tag:<content>`` syntax into clean XML for prompts

Quick Start
-----------

Install super-pocket:

.. code-block:: bash

   pip install super-pocket

Render a markdown file:

.. code-block:: bash

   pocket markdown render README.md

Export your project:

.. code-block:: bash

   pocket project to-file -p . -o project.md

Why super-pocket?
-----------------

super-pocket consolidates common developer tools into a single package, providing:

- **Consistency**: Unified CLI interface across all tools
- **Productivity**: Quick access to frequently-used utilities
- **Extensibility**: Easy to add new tools and templates
- **Quality**: Well-tested, documented, and maintained codebase

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   installation
   quickstart

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   commands
   readme-generator
   templates

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api
   modules

.. toctree::
   :maxdepth: 2
   :caption: Development

   contributing
   testing
   documentation

.. toctree::
   :maxdepth: 1
   :caption: Additional Information

   changelog
   license

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
