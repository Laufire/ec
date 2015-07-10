"""
__main__.py
===========

The console entry point of ec. It could both be used as a script or a python module.

Example:

  $ ec script.py [...]
  
  $ python -m ec script.py [...]

"""
def main():
  import sys
  argv = sys.argv[1:]
  
  if not argv:
    show_usage()
    
  else:
    from os import path
    from modules import core
    from modules.helpers import load_module
    
    target_path = argv.pop(0)
    
    if path.isfile(target_path):
      core.start(load_module(target_path), argv)
      
    elif path.isdir(target_path): # launch the dir with its children as groups
      from glob import glob
      from modules.classes import Group
      
      class Container: # a class to emulate a module
        def __init__(self, Modules):
          for Module in Modules:
            setattr(self, Module.__name__, Module)
        
      Container = Container([load_module(name) for name in glob('%s/*.py' % path.abspath(target_path)) if path.isfile(name)])
      
      Group(Container, {'name': target_path}) # brand the Container
      
      core.start(Container, argv)
      
    else:
      show_usage()
  

def show_usage():
  print 'Usage:\n\t$ ec script/dir [flag] [command] [args]'

if __name__ == '__main__':
  main()