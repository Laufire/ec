import os

from ec.ec import task, arg, group
from ec.types.basics import yn
from ec.types import path as path_type

from modules.helpers import shell_exec, rmtree, get_relative, run, make_link, rmdir, err

# Globals
project_root = get_relative(__file__, '/../')

# Tasks
@task(desc='Lints the source.')
@arg(type=path_type.exists)
def lint(target=None):
  from glob2 import glob

  devLinks.clear()

  if not target:
    for item in ['ec', 'tests'] + glob('Scripts/**/*.py'):
      assert(run('pylint --rcfile=.pylintrc "%s"' % item) == 0)

  else:
    assert(run('pylint --rcfile=.pylintrc "%s"' % target) == 0)

  devLinks.create()


@task(desc='Installs ec.')
def install():

  rmtree('%s/build' % project_root)

  for command in ['build', 'install']:
    assert(run('python setup.py %s' % command) == 0)


@task(desc='Tests the package.')
def test(name=None):
  """
  Args:
    name (str): The name of the test (the string after 'test_'). When a name isn't specified all tests will be done.
  """
  if name:
    assert(run('python tests/test_%s.py' % name) == 0)

  else:
    devLinks.clear() # clear all the dev links to avoid module mixing
    install()
    assert(run('python setup.py test') == 0)
    devLinks.create()


@group(desc='Doc handling tasks.')
class docs:

  @task(desc='Check the docs for spelling mistakes.')
  def spellcheck():

    assert(run('sphinx-build -b spelling -d _build/doctrees  . _build/_spelling', cwd='docs') == 0)


  @task(desc='Check the docs for errors.')
  def check():

    assert(run('rst-lint README.rst') == 0)


  @task(desc='Makes the docs.')
  @arg(type=yn)
  @arg(type=yn)
  def make(check=True, update=False):

    if check:
      docs.check()

    if not update:
      rmtree('docs/_build')

    assert(run('sphinx-build -b html -d _build/doctrees  . _build/html', cwd='%s/docs' % project_root) == 0)


  @task(desc='Upload the doc to PyPI.')
  def upload():

    docs.check()
    assert(run('python setup.py upload_sphinx') == 0)


@group(desc='Packaging tasks.')
class pkg:

  @task(desc='Make the package.')
  def make():

    for dir in ['build', 'dist']: # Clean the build related dirs
      rmtree(dir)

    test()

    devLinks.clear()
    Result = shell_exec('python setup.py sdist')
    devLinks.create()

    try:
      assert(Result['code'] == 0)

      print 'dist done!'

    except Exception: #pylint: disable=W0703
      err(Result['err'], Result['code'])


  @task(desc='Uploads the package to PyPI.')
  def upload():

    assert(run('python setup.py sdist upload') == 0)


  @task(desc='Tests the deployed package (from PyPI).')
  def test(name=None):

    devLinks.clear() # clear all the dev links to avoid module mixing
    assert(run('pip uninstall -y ec') == 0)
    assert(run('pip install --upgrade ec') == 0)
    assert(run('python setup.py test') == 0)
    devLinks.create()


@task(desc='Pushes the repo to origin.')
def push():

  assert(run('git push origin master') == 0)

@group(desc='Create / Clear devLinks.')
class devLinks:
  """Handles the linking to the package dir from various dev dirs, so that the package under development can be the source of ec.
  """
  pkgPath = 'ec'

  EcDirs = [
    'scripts/examples', 'scripts/examples/advanced', 'scripts/tests',
    'tests', 'tests/support', 'tests/targets',
    'tools', '.trial'
  ]

  @task(desc='Creates link to the main ec dir for developing convinience.')
  def create(dir=None):
    """
    Args:
      dir (str): The target dir to create the link in. When no target is specified, all devLinks.EcDirs are considered as the targets.
    """
    if dir:
      devLinks.linkEc(dir)

    else:
      for dir in devLinks.EcDirs:
        devLinks.linkEc(dir)


  @task(desc='Clears the links to the ec dir, under all devLinks.EcDirs.')
  def clear():
    for dir in devLinks.EcDirs:
      rmdir('%s/ec' % dir)

  # Helpers
  def linkEc(dir):
    make_link('ec', '%s/ec' % dir)

# Main
os.chdir(project_root) # ensure that the project_root is the CWD
