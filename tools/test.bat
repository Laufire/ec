@echo off

call tools\install.bat

cd tests

set errorlevel=
set RC=
setlocal
call nosetests
endlocal & set RC=%ERRORLEVEL%

cd ..

exit /B %RC%

@echo on
