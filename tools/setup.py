"""
Installs the required modules for this tools.
"""  
import os
from os.path import dirname
from ec.utils import get
from ec.types.basics import yn

def main(): # from: http://stackoverflow.com/questions/12966147/how-can-i-install-python-modules-programmatically-through-a-python-script
  
  if not get(desc='Running this task might reinstall existing packages. Do you want to continue (y/n)?', type=yn):
    return
  
  import pip

  pip_args = ['install', '-r', 'build_requirements.txt']
  
  proxy = os.environ.get('http_proxy')
  if proxy:
    pip_args = ['--proxy', proxy] + pip_args
  
  if pip.main(pip_args):
    raise Exception('Failed to install %s' % requirement)
    

if __name__ == '__main__':
  os.chdir(dirname(__file__))
  main()