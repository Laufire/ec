ToDo
=====

* Test for cross environment compatibility.

* Add usage document for shell mode.

* Add api docs and more docstrings.

Fix
---

* In API docs the decorators task, arg, group etc are listed as functions.

Check
-----
* Automatically adding params to the doc string.

* ^X in shell mode displaying help.

Later
-----
* Making the name arg, of the decorator, optional. This could be achieved through iterating over the FuncArgs.

* An autodoc extension, to document tasks and groups instead of methods and classes: There are some issues with using autodoc, for example a renamed task is still being documented under the original function name.

* Externally adding params to modules that weren't designed for ec.
