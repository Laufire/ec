import os

from ec.ec import task, arg, group, module, start
from ec.types.basics import yn
from ec.types import path as path_type

from modules.helpers import shell_exec, rmtree, get_relative, run

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
  install()
  
  if name:
    assert(run('python tests/test_%s.py' % name) == 0)
    
  else:
    assert(run('python setup.py test') == 0)
  
@task
def spellcheck():
  os.chdir('%s\docs' % project_root)
  assert(run('sphinx-build -b spelling -d _build/doctrees  . _build/_spelling') == 0)
  os.chdir(project_root)

@task
@arg(type=yn())
def makeDocs(update=False):
  os.chdir('%s\docs' % project_root)
  
  if not update:
    rmtree('_build')
    
  assert(run('sphinx-build -b html -d _build/doctrees  . _build/html') == 0)
  os.chdir(project_root)
  
@task
def dist():
  # Clean the build related dirs
  for dir in ['build', 'dist']:
    rmtree(dir)

  # Shell the build commands
  for command in ['build', 'install', 'test', 'sdist']:
    assert(shell_exec('python setup.py %s' % command)['code'] == 0)
    print '%s done' % command
    
@task
def uploadPkg():
  assert(run('python setup.py sdist upload') == 0)

@task
def push():
  assert(run('git push origin master') == 0)

@task
def uploadDocs():
  assert(run('python setup.py upload_sphinx') == 0)

start(dev_mode=True) # we need a detailed trace, hence this is a developer tool.
