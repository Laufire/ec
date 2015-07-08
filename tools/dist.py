if __name__ != '__main__':
  exit()

import os
from modules.helpers import shell_exec, rmtree, get_relative

parent_dir = get_relative(__file__, '/../')
os.chdir(parent_dir)

# Clean the build related dirs
for dir in ['build', 'dist']:
  rmtree(dir)

# Shell the build commands
for command in ['build', 'install', 'test', 'sdist']:
  assert(shell_exec('python setup.py %s' % command)['code'] == 0)
  print '%s done' % command
  
print """\nDist build done.\n
	Use the following command to upload the package to PyPI:\n
	python setup.py sdist upload
  """