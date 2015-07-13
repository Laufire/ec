Dev Notes
=========

Gotchas
-------
If tests fail for seemingly no reason, try to clear the devLinks and test again (use the tasks devLinks/clear and devLinks/create).

Notes
-----
* Check tools\main.py for automated tasks.

* All the tests should have the project root as their cwd.

* When launching tests manually, some tests might fail due the loading of two ec instances, one from the installation and another from symlinks used for development convenience. Hence the results of the tests done through **tools\test.bat** is final.
