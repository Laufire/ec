ToDo
=====
Tasks
-----
* The long description of the package seems to be broken on PyPI (Could it be because of the code block?).

* Test for cross environment compatibility.

* Add usage document for shell mode.

* Add api docs and more docstrings.

* Test custom types (doctest?).

* Make nut_shell.py as the target_script for the tests.

* More documentation for the custom types.

Issues
------

* Could not exit cleanly from the shell mode of ec, when launching dirs. EOFError is not handled well.

Fix
---

* In the API docs - the decorators, task, arg, group etc are listed as functions.

Check
-----
* Allowing name-less args, especially for a better UX in the shell mode. There are several ways, including:
  
  * Allowing the first argument of a task to be name-less.
  * Allowing tasks with a single arg to have name-less inputs.

* Automatically adding params to the doc string.

* ^X in shell mode displaying help on the arg being collected.

Later
-----
* An autodoc extension, to document tasks and groups instead of methods and classes: There are some issues with using autodoc, for example a renamed task is still being documented under the original function name.

* Externally adding params to modules that weren't designed for ec.
