Dev Notes
=========

Notes
-----
* There are some batch scripts available at **ec\tools** to automate repeated tasks.

* All the tests should have the root dir, **ec** as their cwds.

* When launching tests manually, some tests might fail due the loading of two ec instances, one from the installation and another from symlinks used for development convinience. Hence the results of the tests done through **tools\test.bat** is final.
