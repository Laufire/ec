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
    
    sys.argv = sys.argv[:1] + argv # alter sys.argv so that the modules could process them
    
    if path.isfile(target_path):
      core.start(load_module(target_path), argv)
      
    elif path.isdir(target_path): # launch the dir with its children as groups
      from glob import glob
      
      from ec import member # ec has to be imported in order to make the import hook work
      
      for Module in [load_module(module_path) for module_path in glob('%s/*.py' % path.abspath(target_path)) if path.isfile(module_path)]:
        __ec_member__ = getattr(Module, '__ec_member__', None)
        
        if __ec_member__: # register only modules that are designed for ec
          member(Module)
      
    else:
      show_usage()  

def show_usage():
  print 'Usage:\n\t$ ec script/dir [flag] [command] [args]'

if __name__ == '__main__':
  main()
  