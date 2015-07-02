.. :changelog:

History
=======
0.1.0 (2015-06-01)
---------------------

Log
---
* 20150623

  * 1739  Scaffolded from the template **laufire-py-package, v0.1.0**.
  * 2355  Preparation done.
  
* 20150625

  * 1000  Decided to use a single dictionary arg as the way to provide data to the functions, over using multiple args (the commom python way), as the former is more elegant. And also because kwargs aren't availabe on other platforms, thus making the implementation of the API, hard.
  * 1745  The development of the libray is suspended, as the intented imporovements over commander are added to commander itself.
  
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
  * 1640  Made private embeddable.
  * 1820  Made private completly embeddable.
  * 1820  Documented nut_shell.py using sphinx autodoc.
  * 1900  Class based groups could now have private members.
  * 1915  Redid the entry points. **private** could now be used to launch scripts.
  * 2005  **private** could now be used to launch all the scripts in a dir.
  * 2050  Linted the scripts.
  
* 20150701

  * 0100  Extraceted the workers from the decorators in config.py. It is done in order to avoid reparring the workers over and over.
  * 0330  Added a custom type **types.regex.pattern**. It took ~20 mins.
  * 0515  Unknown args are now filtered out.
  * 0520  Added a custom type lib **types.multi**, that helps with inputs related to lists.
  * 2100  Class, CustomType introduced.
  * 2130  Changed input string generation process of the variables.
  * 2240  Added private.call, that allow the calling of tasks with partial inputs.
  * 2315  Added a custom type **types.basics.yn**.
  
* 20150702
  
  * 0055  Added a custom type **types.adv.t2t**, which could convert private args into custom types.
  * 0140  Dispatch mode now supports flags.
  * 0145  Dispatch mode flag -p introduced to allow sending partial args to the executing command.
  * 0345  private scripts could now be wrapped (by other modules to provide extended functionality, like a GUI etc).
  * 0520  Added interface.py to help with wrapping private.
  * 0550  helper_tasks.py introduced.
  * 0750  Wrote some tests.
  