Documentation Guide
===================

This guide explains how to build, preview, and publish Super Pocket's documentation
with Sphinx locally and Read the Docs (RTD) in production.

Local Sphinx Workflow
---------------------

1. **Create a virtual environment (recommended):**

   .. code-block:: bash

      python -m venv .venv
      source .venv/bin/activate

2. **Install the documentation dependencies:**

   .. code-block:: bash

      pip install -r docs/requirements.txt

3. **Build the HTML site:**

   .. code-block:: bash

      cd docs
      make html
      # View it
      open _build/html/index.html  # macOS

4. **Enable live reload while editing:**

   .. code-block:: bash

      make livehtml  # Requires sphinx-autobuild

5. **Lint links and references before pushing:**

   .. code-block:: bash

      make linkcheck

Autodoc & API Pages
-------------------

* ``docs/conf.py`` already enables ``autodoc`` and ``autosummary``.
* Add new modules to ``docs/api.rst`` and ``docs/modules.rst`` so Sphinx and RTD pick them up.
* Keep docstrings in English and prefer Google-style formatting for best rendering.
* When adding modules, ensure they are importable (use ``if TYPE_CHECKING`` guards if heavy dependencies are optional).

Read the Docs Configuration
---------------------------

Super Pocket is published at https://pocketdocs.readthedocs.io/. To keep builds green:

* **Project settings**

  - Repository: ``main`` branch
  - Documentation type: Sphinx HTML
  - Python version: 3.11+
  - Install requirements: ``docs/requirements.txt`` (configured under *Advanced settings → Python → Requirements file*)

* **Build command**

  RTD automatically invokes ``sphinx-build -b html docs/ docs/_build/html``. No custom command is needed as long as ``conf.py`` lives in ``docs/``.

* **Environment variables**

  Add any secrets (for example API keys used in code examples) through the RTD dashboard. Do **not** commit them to the repo.

* **Versioning**

  Tag releases (``v1.0.2``, etc.) so RTD can produce versioned docs. Enable the *"Activate on tag"* option if you want automatic builds per release.

Pre-Publish Checklist
---------------------

Run these commands locally before opening a PR that touches documentation:

.. code-block:: bash

   # Clean previous builds to avoid stale assets
   make -C docs clean

   # Fails on warnings to mimic RTD's stricter settings
   sphinx-build -n -W --keep-going -b html docs/ docs/_build/html

   # Verify external links (can be slow, so only when needed)
   make -C docs linkcheck

Troubleshooting
---------------

* **Module import errors:** Confirm ``sys.path`` in ``docs/conf.py`` points to the repo root. Keep runtime-only dependencies optional or mock them in docs builds.
* **Theme/CSS not applied on RTD:** Ensure files under ``docs/_static`` are tracked and referenced via ``html_css_files``.
* **Missing API entries:** Update ``docs/api.rst`` or ``docs/modules.rst`` and rebuild with ``make html`` to refresh the autosummary stubs.
* **Build succeeds locally but fails on RTD:** Re-run builds using ``sphinx-build -n -W`` to treat warnings as errors and catch the same issues locally.

Next Steps
----------

* :doc:`installation` - Install Super Pocket and its optional extras.
* :doc:`contributing` - Contribution guidelines, including documentation expectations.
* :doc:`commands` - High-level CLI overview once docs are published.

