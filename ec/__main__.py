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
      import imp
      from glob import glob
      from collections import OrderedDict
      
      from modules.classes import Group
      
      Container = imp.new_module(target_path)
      Members = OrderedDict()
      
      for Module in [load_module(module_path) for module_path in glob('%s/*.py' % path.abspath(target_path)) if path.isfile(module_path)]:
        __ec_member__ = getattr(Module, '__ec_member__', None)
        if __ec_member__: # register only modules that are designed for ec
          __ec_member__.__load_members__()
          name = Module.__name__
          print Module, name, '--------'
          setattr(Container, name, Module)
          Members[name] = __ec_member__
      
      BaseGroup = Group(Container, {'name': target_path}) # brand the Container
      BaseGroup.Config['Members'] = Members
      
      '''
      class Container: # a class to emulate a module
        def __init__(self, Modules):
          for Module in Modules:
            if hasattr(Module, '__ec_member__'): # register only modules that are designed for ec
              setattr(self, Module.__name__, Module)
      Container = Container()
      '''
      
      BaseGroup.__load_members__()
      core.start(Container, argv)
      
    else:
      show_usage()  

def show_usage():
  print 'Usage:\n\t$ ec script/dir [flag] [command] [args]'

if __name__ == '__main__':
  main()