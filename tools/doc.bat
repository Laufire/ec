@echo off

cd docs

REM sphinx-apidoc -o ./_autodoc ../scripts/examples/ -f -E

call make html

cd ..

@echo on