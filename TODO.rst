ToDo
=====
Tasks
-----
* Test for cross environment compatibility.

* Add usage document for the UI. ie: shell mode, partial args, positonal args etc.

* Add api docs and more docstrings.

* Test all the cases of HandledException-s.

* Test custom types (doctest?).

* Make nut_shell.py as the target_script for the tests.

* More documentation for the custom types.

Features
--------

* **-t**, a dispatch mode flag to show the entire command tree.

Issues
------

* *None, yet.*

Fix
---

* In the API docs - the decorators, task, arg, group etc are listed as functions.

Check
-----
* A ec.main decorator to act as the entry point for the modules, to allow the pre-processing of the modules etc.

* Reallowing **None** values as args. It might be done using escape sequences like **\0**. **Caution:** it might not be advisable to allow them, as no other cli seems to allow **None** as an argument.

* Allowing name-less (positional) args, especially for a better UX in the shell mode. There are several ways, including:
  
  * Allowing the first argument of a task to be name-less.
  * Allowing tasks with a single arg to have name-less inputs.

* Automatically adding param documentation to docstrings.

* A main command (as in commandify) for the module, so that a task name won't be necessary. This might be implemented in several ways:

  * A separate config decorator (@default).
  * Treating the only / first command as the default command.
  * Instructing the user to use **ec.call** on the default function. This would require the handling of the command line arguments.

* ^X in shell mode displaying help on the arg being collected.

* Extensions:

  * Automatic aliases.
  
  * An **all** task on groups, with ***** as thier alias.
  
Later
-----
* An autodoc extension, to document tasks and groups instead of methods and classes: There are some issues with using autodoc, for example a renamed task is still being documented under the original function name.

* Externally adding params to modules that weren't designed for ec.
