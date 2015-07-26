History
=======
v0.2.1 (2015-07-25 1340 +0530)
------------------------------

Log
---
* 20150623

  * 1739  Scaffolded from the template **laufire-py-package, v0.1.0**.
  * 2355  Preparation done.
  
* 20150625

  * 1000  Decided to use a single dictionary arg as the way to provide data to the functions, over using multiple args (the common python way), as the former is more elegant. And also because kwargs aren't available on other platforms, t2hus making the implementation of the API, hard.
  * 1745  The development of the library is suspended, as the intended improvements over commander are added to commander itself.
  
* 20150629

  * 1440  Resumed the development.
  * 1740  Dispatch mode completed.
  * 2200  Shell mode completed.
  * 2200  It tool ~7hrs to implement a working prototype, most of the time went to developing the details.
  * 2300  Added scripts/examples/nut_shell.py.
  * 2305  Added scripts/tests/config.py.
  
* 20150630

  * 0105  Found that sphinx-autodoc cannot document objects of custom classes.
  * 0135  Generated some primitive documentation for nut_shell.py using autodoc.
  * 1640  Made ec embeddable.
  * 1820  Made ec completely embeddable.
  * 1820  Documented nut_shell.py using sphinx autodoc.
  * 1900  Class based groups could now have ec members.
  * 1915  Redid the entry points. **ec** could now be used to launch scripts.
  * 2005  **ec** could now be used to launch all the scripts in a dir.
  * 2050  Linted the scripts.
  
* 20150701

  * 0100  Extracted the workers from the decorators in config.py. It is done in order to avoid re-parsing the workers over and over.
  * 0330  Added a custom type **types.regex.pattern**. It took ~20 mins.
  * 0515  Unknown args are now filtered out.
  * 0520  Added a custom type lib **types.multi**, that helps with inputs related to lists.
  * 2100  Class, CustomType introduced.
  * 2130  Changed input string generation process of the variables.
  * 2240  Added ec.call, that allow the calling of tasks with partial inputs.
  * 2315  Added a custom type **types.basics.yn**.
  
* 20150702
  
  * 0055  Added a custom type **types.adv.t2t**, which could convert ec args into custom types.
  * 0140  Dispatch mode now supports flags.
  * 0145  Dispatch mode flag -p introduced to allow sending partial args to the executing command.
  * 0345  ec scripts could now be wrapped (by other modules to provide extended functionality, like a GUI etc).
  * 0520  Added interface.py to help with wrapping ec.
  * 0550  helper_tasks.py introduced.
  * 0750  Wrote some tests.
  * 1405  Added TODO.rst.
  * 1535  Added tools/spellcheckbat.
  * 1620  Added tools/dist.bat.
  * 1655  Pushed to github.
  * 1735  Registered the package at PiPy.
  * 2145  Shell mode now supports **None** inputs, through the \0 (^z) char.
  * 2005  Command routes are now separated by '/', instead of ' '; in order to closely emulate query strings.
  * 2005  Dispatch mode now supports **None** inputs, through omitted '=' signs after the arg names. ie: in *task1 a b=1*, the value of **a** will be **None**.
  
* 20150703
  
  * 1830  Tuned config processing to be cleaner.
  * 1925  Aliases introduced.
  * 1935  docs/dev_notes.rst added.
  
* 20150704
  
  * 1310  Introduced ec.utils, with a set of utility functions for the scripts.
  * 1340  Introduced ec.utils.get, that helps to interactively get user input.
  * 1355  Renamed the module, ec.ec to ec.config.
  * 1645  Tuned the handling of description strings.
  * 1705  Bug fixed: -h flag in the dispatch mode wasn't working.
  
* 20150705
  
  * 2145  Renamed the module, ec.config back to ec.ec, as it felt more apt .
  * 2310  Added __info__.py.
  
* 20150706

  * 0045  Added types.multi.menu.
  * 0050  v0.1.1 released.
  * 0350  Replaced tools/dist.bat with tools/dist.py (the former was buggy).
  * 0050  v0.1.2 released. Though no changes were made to the package, it wasn't possible to upload the module (because of a previously missing file), to PyPI with the same version string.
  * 1545  Tried, but failed to automate the building of README.rst with sphinx, to be used as the long_description for the package (which would be used as the home page in PyPI); as there wasn't a way to dynamically generate rst-s fr static rst files.
  * 1725  Altered README.rst to fit PyPI.
  * 1725  Added tools/upload_docs.bat.
  * 1805  Found that stdin could be used to test the shell mode.
  
* 20150708

  * 1830  Made the name arg of the decorator, arg, optional.
  * 1840  Switched to google-style docstrings.
  * 1950  Added more docstrings.
  * 2100  v0.1.3 released.
  * 2335  Removed ec calls from the exception tracebacks of the scripts, to make the traceback more understandable. It took ~1:30 hrs to finish it, owing mostly to the inexperience with tracebacks.
  
* 20150709

  * 0205  Tuned the error reporting process (~30 mins).
  * 0415  Tried, but failed to arrange the members in their order of declaration, due to the failure in finding the lineno for the classes (it was found for functions in co_firstlineno).
  * 0500  Added types.path.
  * 0520  Added types.adv.chain.
  * 0540  Bug fixed: arg configurations without names weren't processed properly.
  * 0600  Replaced tools\*.bat with tools\main.py, an ec based script.
  * 0645  v0.1.4 released.
  * 0730  Added types.adv.invert.
  * 2115  Members are added in an orderly fashion.
  
* 20150710

  * 0105  Added tests\test_dir_group.py.
  * 0520  Tried, but failed to make tasks inside groups to be callable, like **group1.task1(...)**. ~2 hrs of tinkering couldn't make the unbound methods into functions.
  * 0705  Added tests\test_shell.py.
  * 0930  All the methods of the groups are converted to static methods, to facilitate easier calling.
  * 1945  Introduced modules.exposed.
  * 1950  Conversion of static methods has been moved from ec.core to ec.modules.exposed. The functionality is now exposed as **utils.static**.
  * 1950  Nested modules made to work.

* 20150712

  * 0500  Moved helper_tasks.listMemberHelps to helper.listMemberHelps, to avoid importing helper_tasks in the dispatch mode.

* 20150713

  * 0050  modules.state introduced.
  * 0500  Removed ec.start, the scripts now just have to import ec, to be considered an ec script.
  * 0500  Introduced ec.settings to replace ec.start as the settings provider.
  * 1805  Moved shell helpers, clear and help to '/', with an option to move them inside a group through **ec.settings.helper_route**.
  * 2250  Partially redid the core (member classification) to support the new API. Neseted modules and launching dirs aren't supported yet.
  
* 20150714

  * 0400  Introduced modules.config.member to allow the addition of imported members to scripts.
  * 0425  Nested modules now support the newer API.
  * 0720  Dir launching now supports the newer API.
  
* 20150715
  
  * 1700  Separated the hooks from ec.ec into modules.hooks.
  
* 20150716
  
  * 0305  Redid the core to support the new API.
  * 0500  Simplified the static method conversions of the groups.
  * 0725  Tuned and linted.
  * 0900  Added test_utils.py.
  * 0955  Made README.rst to be compatible with PyPI. To ensure compatibility the file is now linted before uploads.
  * 1945  Bug fixed: In modules.hooks.hookIntoImport.newImp module names weren't processed correctly.
  
* 20150717

  * 0945  Bug fixed: Exiting from exit hook (from the shell mode) caused errors, when stdlib.threading is imported. It took ~5hrs, of which ~4hrs is spent to spot the bug.
  * 1030  __info__.py removed.
  * 1535  Bettered import hooking.
  * 1610  Added tests\test_configuration.py.
  * 1925  Added tests\test_entry_point_launch.py.
  * 2100  Added tests\test_module_launch.py.
  * 2200  v0.2.0 released with changes to the API.
  
* 20150718

  * 0220  Bettered tools\main.py
  
* 20150722

  * 2240  Added **force_config**, **add** to ec.interface.
  
* 20150723

  * 0045  ec.interface.call now passes the raised exceptions to the calling script; previously it was processed within ec.  
  * 1035  Bettered help on both modes.
  * 1235  Mode, dispatch, now shows help on some HandledException-s.
  
* 20150725

  * 1200  Removed the ways to pass **None** as the value for args, as the existing command line format, which allows *None* as values meddled didn't allow positional args. As of now the only way to have **None** values is to pass them as the defaults of the configs.
  * 1335  Positional args are supported. It took ~3hrs, mainly due to the change being very close to the core (4 modules had to be altered).
  * 1340 v0.2.1 released.
  
* 20150726

  * 0035  Bug Fixed: Default value and labels in ex.types.basics.yn weren't handled properly.
  