# -*- coding: utf-8 -*-

def main():
  import sys
  from modules import helpers
  argv = sys.argv[1:]
  
  if not argv:
    helpers.show_usage()
    
  else:
    from os import path
    from modules import core
    
    target_path = argv.pop(0)
    
    if path.isfile(target_path):
      core.start(helpers.load_module(target_path), argv)
      
    elif path.isdir(target_path):
      from glob import glob
      from modules.classes import Group
      
      class Container: # a class to emulate a module
        def __init__(self, Modules):
          for Module in Modules:
            setattr(self, Module.__name__, Module)
        
      Container = Container([helpers.load_module(name) for name in glob('%s/*.py' % path.abspath(target_path)) if path.isfile(name)])
      
      Group(Container) # brand the Container
      
      core.start(Container, argv)
      
    else:
      helpers.show_usage()
  

if __name__ == '__main__':
  main()