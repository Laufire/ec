import os

from ec.ec import task, arg, group, module, settings
from ec.types.basics import yn
from ec.types import path as path_type

from modules.helpers import shell_exec, rmtree, get_relative, run, make_link, rmdir, err

# Globals
project_root = get_relative(__file__, '/../')

os.chdir(project_root) # ensure that the project_root is the CWD

@task
@arg(type=path_type.exists)
def lint(target=None):
  
  if not target:
    assert(run('cmd /c pylint --rcfile=ec/.pylintrc ec') == 0)
    
  else:
    assert(run('cmd /c pylint --rcfile=ec/.pylintrc "%s"' % target) == 0)
  
@task
def install():
  rmtree('%s/build' % project_root)
  
  for command in ['build', 'install']:
    assert(run('python setup.py %s' % command) == 0)
  
@task
def test(name=None):
  """Tests the package.
  
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

@group
class docs:
  @task
  def spellcheck():
    os.chdir('%s\docs' % project_root)
    assert(run('sphinx-build -b spelling -d _build/doctrees  . _build/_spelling') == 0)
    os.chdir(project_root)

  @task
  @arg(type=yn())
  @arg(type=yn())
  def make(check=True, update=False):
    os.chdir('%s\docs' % project_root)
    
    if check:
      docs.check()

    if not update:
      rmtree('_build')
    
    assert(run('sphinx-build -b html -d _build/doctrees  . _build/html') == 0)
    os.chdir(project_root)
    
  @task
  def check():
    assert(run('rst-lint README.rst') == 0)

  @task
  def upload():
    docs.check()
    assert(run('python setup.py upload_sphinx') == 0)
  
@group
class pkg:
  @task
  def make():
    # Clean the build related dirs
    for dir in ['build', 'dist']:
      rmtree(dir)

    test()
    
    Result = shell_exec('python setup.py sdist')
    
    try:
      assert(Result['code'] == 0)
      
      print 'dist done!'
      
    except Exception :
      err(Result['err'], Result['code'])
      
  @task
  def upload():
    assert(run('python setup.py sdist upload') == 0)
    
  @task
  def test(name=None):
    """Tests the deployed package (from PyPI).
    """
    devLinks.clear() # clear all the dev links to avoid module mixing
    assert(run('pip uninstall -y ec') == 0)
    assert(run('pip install --upgrade ec') == 0)
    assert(run('python setup.py test') == 0)
    devLinks.create()

@task
def push():
  assert(run('git push origin master') == 0)
  
@group
class devLinks:
  """Handles the linking to the package dir from various dev dirs, so that the package under development can be the source of ec.
  """
  pkgPath = 'ec'
  
  Dirs = [
    'scripts/examples', 'scripts/examples/advanced', 'scripts/tests',
    'tests', 'tests/support', 
    'tools', '.trial'
  ]
  
  @task
  def create(dir=None):
    """Creates link to the main ec dir for developing convinience.
    
    Args:
      dir (str): The target dir to create the link in. When no target is specified, all devLinks.Dirs are considered as the targets.
    """
    if dir:
      devLinks.linkEc(dir)
      
    else:
      for dir in devLinks.Dirs:
        devLinks.linkEc(dir)
        
  @task
  def clear():
    """Clears the links to the ec dir, under all devLinks.Dirs.
    """
    for dir in devLinks.Dirs:
      rmdir('%s/ec' % dir)
  
  def linkEc(dir):
    make_link('ec', '%s/ec' % dir)
    
settings(dev_mode=True) # we need a detailed trace, hence this is a developer tool.
