@echo off

cd docs

sphinx-build -b spelling -d _build/doctrees  . _build/_spelling

cd ..

@echo on