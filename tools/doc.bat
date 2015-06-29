cd docs

sphinx-apidoc -o ./_autodoc ../scripts/examples/ -f

call make html

cd ..
