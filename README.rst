private
========

private - a simpler, yet better implementation of Commander, a module launcher.

* Free software: MIT license

  **Note: The docs serve as a reference, as well as act as a design guide throught the alpha version. Hence incase of an inconsistency, assume it as a work in progress.**
  
Features
--------
* Shell and Dispatch modes.

* Typed params.

* Every param is to be input, separately; with every query having a description, default value etc.

ToDo
----
* Make private wrappable; ie: implement private.call.

* Implement helper tasks.

Check
-----
* Automatically adding params to the doc string.

Later
-----
* Add usage document for shell mode.

* Add api docs and more docstrings.

* Making the name arg, of the decorator, arg optional. This could be achived through iterating over the FuncArgs.

* An autodoc extension, to document tasks and groups instead of methods and classes: There are some issues with using autodoc, for example a renamed task is still being documented under the original function name.
