@echo off

python setup.py sdist

cd dist

for %%x in (*.zip) do if not defined firstFile set "firstFile=%%x"

rd /S /Q ec

7z x %firstFile% -oec

cd ec

FOR /f "tokens=*" %%x in ('DIR /a:d /b *') do if not defined baseDir set "baseDir=%%x"

cd %baseDir%

python setup.py install

set errorlevel=
set RC=
setlocal

python setup.py test

endlocal & set RC=%ERRORLEVEL%

cd ..\..\..

if %RC% == 0 ( echo done ) else (

	echo failed
	exit /B %RC%
)

@echo on
