Quick Start Guide
=================

A fast, hands-on tour of Super Pocket with concrete commands and outputs. Keep your terminal open—everything below is copy/paste ready.

Interactive mode (the easy way)
-------------------------------

Not sure where to start? Just type:

.. code-block:: bash

   pocket

This launches an interactive menu that guides you through all available tools. Use it to explore features without memorizing commands. Type ``exit`` or ``Q`` to quit.

First sanity check
------------------

.. code-block:: bash

   pocket --help

You should see the menu of groups (markdown, project, documents, pdf, web, readme, xml). If that shows up, you're good.

Render Markdown (pretty output)
-------------------------------

.. code-block:: bash

   pocket markdown render README.md -w 100
   # or the alias
   markd README.md

What you’ll see: headings aligned, code blocks highlighted, and lists spaced nicely—no raw ``#`` or messy bullets.

Export the whole project to one file
------------------------------------

.. code-block:: bash

   pocket project to-file -p . -o project-all-in-one.md \
     -e ".git,venv,node_modules"

Output: a single Markdown with the tree + every file inline. Perfect to drop into an LLM or share for a quick review.

Generate a README in minutes
----------------------------

Interactive wizard:

.. code-block:: bash

   pocket project readme -p . -o README.md

Direct mode (no Q&A):

.. code-block:: bash

   pocket readme analyze -p .
   pocket readme generate -p . -o README.md

Result: a push-ready README with sections matched to your stack.

Spot outdated dependencies
--------------------------

.. code-block:: bash

   pocket project req-to-date requirements.txt
   pocket project req-to-date numpy==1.23,rich>=13 pyproject.toml

Expect lines like ``fastapi 0.110.0 -> 0.121.3`` (red for old, green for fresh).

Spin up a starter project
-------------------------

.. code-block:: bash

   pocket project init list
   pocket project init show fastapi-basic
   pocket project init new fastapi-basic --quick -p ./demo-api

You get a scaffolded project folder with sensible defaults, plus validation for names/paths.

Templates & cheatsheets on tap
------------------------------

.. code-block:: bash

   pocket documents list
   pocket documents view unit_tests_agent
   pocket documents copy unit_tests_agent -o .AGENTS/
   pocket documents init -o .AGENTS

Great for stocking a repo with AGENTS.md templates or quick references.

PDF and web helpers
-------------------

.. code-block:: bash

   pocket pdf convert README.md -o README.pdf
   pocket web favicon logo.png -o favicon.ico --sizes "64x64,32x32"
   pocket web job-search "python developer" --work_from_home -o jobs.json

Remember: ``web job-search`` needs ``RAPIDAPI_API_KEY`` exported in your env.

LLM-friendly XML
----------------

.. code-block:: bash

   pocket xml "note:hello world"
   pocket xml -f input.txt -o output.xml

If you provide nothing, it prompts interactively and still prints pretty XML.

Common mini-workflows
---------------------

- **Doc-in-a-box:** ``pocket project to-file -o snapshot.md`` → ``pocket pdf convert snapshot.md -o snapshot.pdf``  
- **CI helper:** call the stand-alone shortcuts (``proj2md``, ``markd``, ``conv2pdf``, ``req-update``) directly in pipelines.  
- **Agent setup:** ``pocket documents init -o .AGENTS`` then ``pocket documents view <name>`` to pick the right file.  

Next steps
----------

* :doc:`commands` for the full, friendly reference
* :doc:`documents` to see what ships in the box
* :doc:`installation` if you need extras (web/pdf) or dev setup
