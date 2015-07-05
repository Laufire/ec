@echo off

set errorlevel=

rd /s /q build
rd /s /q dist
REM rd doesn't return a error code

python setup.py build
if %errorlevel% neq 0 exit /b %errorlevel%

python setup.py sdist
if %errorlevel% neq 0 exit /b %errorlevel%

cd dist

for %%x in (*.zip) do if not defined firstFile set "firstFile=%%x"

rd /S /Q ec

7z x %firstFile% -oec
if %errorlevel% neq 0 exit /b %errorlevel%

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

echo --------------------

if %RC% == 0 (

	REM Uploading to pypi... (The package has to be registered first)
	echo Dist build done.
	echo Use the following command to upload the package to PyPI:
	echo python setup.py sdist upload
	
) else (
	
	echo Dist build failed.
	exit /B %RC%
)

@echo on
