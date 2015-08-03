ToDo
=====

Tasks
-----
* Test for cross environment compatibility.

* Make the development possible with other platforms. The current structre depends upon some windows only features like dir junctions.

* Add usage document for the UI. ie: shell mode, partial args, positonal args etc.

* Add usage documents for the API.

* Add a **Change log** file that lists important changes across versions.

* Add api docs and more docstrings.

* Test all the cases of HandledException-s.

* Test custom types (doctest?).

* Extract **sphinxdoc** as a separate package.

* Make nut_shell.py the target_script for the tests.

* More documentation for the custom types.

* More examples. Especially for:

  * Dynamic configuration of CustomTypes.

Later
-----

* **-t**, a dispatch mode flag to show the entire command tree.

* Coverage for tests.

Issues
------
* In the API docs - the decorators, task, arg, group etc are listed as functions.


* Adding a reference to the parent Group on the Members.

* On missing tasks, the help lists the members of the base, instead of the last resolved group.

* Missing scripts does not error. Ex: python -m ec tests/support simple/task1 arg1=1.

Check
-----
* Supporting \*args. Though it's possible to implement it with a minimum effort, the following things need to be considered.
  
  * How to implement \*args in the shell mode? Posibblly using ^Z to specify the ending?
  
  * How to other packages handle \*args? Ex: **argparse.nargs**.
  
* hepler_tasks.reload, which reload the app (while in shell mode), in order to ease development.

* Checking for __init__.py before launching the dirs, to be more pythonic.

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
* Externally adding params to modules that weren't designed for ec.
