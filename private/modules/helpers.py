import sys

def err(message, exit_code=None):
  sys.stderr.write('%s\n' % message)
  
  if exit_code is not None:
    exit(exit_code)
    
def get_calling_module():
  import inspect
  return inspect.getmodule(inspect.currentframe().f_back.f_back) # Check: Could the depency on inspect be avoided?

def load_module(module_path):
  import imp
  from os import path
  
  module_path = path.abspath(module_path)
  parent_path, name = path.split(module_path)
  name, dummy = path.splitext(name)
  
  sys.path.insert(0, parent_path)
  Module = imp.load_source(name, module_path)
  
  return Module

def show_usage():
  err('private module_path <command route> [options]', 1)
  