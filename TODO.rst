ToDo
=====

Tasks
-----

* Document the use of delegates in converting non-ec packages into ec-ed ones.

* Simplify the structure, so that it would be understood easily.

* Fix: Nested groups aren't working as expected.

* Fix: Strings couldn't be set as as default values (as the empty string passed to skip the argument is considered as a valid input).

* The alias c/pb, resolves to the task c, if there's one.

* Fix: String escaping isn't proper, equal signs escaped with slashes weren't properly escaped back.

* Fix: Nested groups fail to be parsed. Having a single neseted, ordered dictionary could solve the issue, by simplifying the structures (the current structcture of traversing through Members seems to be complicated).

* Think of providing type checks as functions, so that they could be used for validation inside the function body. This also could be used to lighten the loads.

* Raise vaule errors (with the proper description), for the first missing, required parameter. As of now, these are raised only when the parameter is of a wrong type.

* Think of lazy intialization types to reduce, load times.

* Try extending the flags silent and debug to utils.get.

* Merge ec.make_type with ec.utils.custom.

* Add a call, named **expose** to expose an existing singletone without configuration.

* Try merging @arg(type) with make_type(func).

* Add an example for **ec.make_type**. Ex: make_type(func=lambda val: val if val > 1 else throw()).

* List all the exports of the type modules under the __all__ variable for easier reference.

* Think of allowing unspecified \*Args and \*\*KWArgs.

* scripts/tests/custom_types isn't working.

* Task routing is not done properly on name collisions. For example, consider a script with a group **t** followed by a task with an alias **t**; calling **t/c** will call the task with **t**, rather than the intended **t/c**.

* Fix: Couldn't exit while loading modules.

* Check for the availability of a TTY brfore entering shell mode.

* Support positional args. With the following guide lines.

	* Collect the args as a tuple under a normal arg, rather than a \*arg. As this would allow the arg to have defaults as well as allow the **@arg** decorator could be used to configure the argument.

	* The *@arg* decorator gets a new kwarg, **count**, a **(min, max)** tuple that represents the number of arguments to be collected. **None** could be used as the value fo min / max. Instead of a tuple a single argument too could be provide which would both be the min and the max values.

	* In the shell mutilple arguments are to be input as *shlex* strings.

	* In the dispatch mode the end of the items is marked with the beginning of the next named arg. This design is to remove the ambiguity when mentioning multiple multi-args. This would also allow the metioning of the first multi-arg without a name, thus enhancing the UX.

	* When the arg has a default, use a tuple instead of a list, as the default lists might be accidentally modified.

* Make tools/main.py cross-platform.

* Test for cross environment compatibility.

* Make the development possible with other platforms. The current structre depends upon some windows only features like dir junctions.

* Add usage document for the UI. ie: shell mode, partial args, positonal args etc.

* Add usage documents for the API.

* Add a **Change log** file that lists important changes across versions.

* Add api docs and more docstrings.

* Test all the cases of HandledException-s.

* Test custom types (doctest?).

* Make nut_shell.py the target_script for the tests.

* More documentation for the custom types.

* More examples. Especially for:

	* Dynamic configuration of CustomTypes.

* Import possible features from Commander. Or better, build a bride or create a separate library (for the wev interface etc).

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
* Passing named before unnamed args, just like named and unamed arg decorators. Though this might ease the input, it could make remembering difficult.

* Replacing the flag, **-h** with a task, **help** (like pip). This would also allow the impementaion of custom help through overriding.

* Optionally turning of the hooks, and requiring an explicit *start_ec()* call to register the members of the modules.

* At entry_hook, might be needed, structurally, as ec is designed to launch multiple scripts. It could have an option to run it only when the script is main, or else it could have another hook named if_main.

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
