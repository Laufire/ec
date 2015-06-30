@echo off

REM usage: ../>tools\lint [dir / .py file]

set argC=0
for %%x in (%*) do Set /A argC+=1

if %argC%==0 (

	pylint --rcfile=private/pylintrc private
	
) else (

	pylint --rcfile=private/pylintrc %*
	
)

@echo on
