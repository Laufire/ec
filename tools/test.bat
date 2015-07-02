@echo off

call tools\install.bat

set errorlevel=
set RC=
setlocal

python setup.py test

endlocal & set RC=%ERRORLEVEL%

exit /B %RC%

@echo on
