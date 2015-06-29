private
========

private - a simpler, yet better implementation of Commander, a module launcher.

* Free software: MIT license

Features
--------
* Shell and Dispatch modes.

* Typed params.

* Every param is to be input, separately; with every query having a description, default value etc.

ToDo
----
* Document an example script using sphix autodoc.

* A separate types library.

Check
-----
* Using private as an embedable, as opposed to a launcher, in order to make it play nice with sphinx-autodoc (autodoc can't use private as a launcher).

* Documenting tasks and groups.

* Automatically adding params to the doc string.

* Returning the underlying of the members insted of the decorated wrappers, so that the modules could be imported into other modules, without side effects. On the other hand, there seems to be little to no chance of importing user facing modules into other modules.

* Private methods within groups; this too will need the exposing of the underlying, as the methods can't be accessed using dynamic __getattr__ calls, because groups are unintantiated classes.

* Making the 'name' arg of the decorator, arg, optional (the name could be got from FuncArgs).
