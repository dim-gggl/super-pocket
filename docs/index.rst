super-pocket
============

.. image:: https://img.shields.io/badge/version-1.0.1-blue.svg
   :alt: Version 1.0.1

.. image:: https://img.shields.io/badge/python-3.11+-blue.svg
   :alt: Python 3.11+

.. image:: https://img.shields.io/badge/license-MIT-green.svg
   :alt: MIT License

**super-pocket** is a comprehensive collection of developer productivity tools that streamline your development workflow.
From beautiful markdown rendering to project exporters, agent templates, and cheatsheets management - Super Pocket brings
essential developer utilities into a single, unified CLI interface.

Features
--------

**Markdown Rendering**
   Beautiful terminal rendering of Markdown files with syntax highlighting and rich formatting

**Project Export**
   Convert entire projects to single Markdown files for easy sharing and documentation

**Agent Templates**
   Manage and distribute AI agent configuration templates for consistent AI-assisted development

**Cheatsheets**
   Quick access to development cheatsheets and reference materials

**PDF Tools**
   Convert markdown and text files to professional PDF documents

**Web Utilities**
   Generate favicons and other web assets from images

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
