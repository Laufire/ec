"""
Helpers

  Generic helpers for the modules.
"""
from types import ClassType, ModuleType, FunctionType
import sys

def err(message, exit_code=None):
  sys.stderr.write('%s\n' % message)
  
  if exit_code is not None:
    exit(exit_code)
    
def get_calling_module():
  return sys.modules[sys._getframe().f_back.f_back.f_locals['__name__']]

def load_module(module_path):
  import imp
  from os import path
  
  module_path = path.abspath(module_path)
  parent_path, name = path.split(module_path)
  name, dummy = path.splitext(name)
  
  sys.path.insert(0, parent_path)
  Module = imp.load_source(name, module_path)
  
  return Module

def list2dict(lst, splitter='='):
  Dict = {}
  
  for item in lst:
    split_pos = item.find(splitter)
    
    if split_pos == -1:
      Dict[item] = None # consider entries without an equal sign as an item with a value of None.
      
    else:
      Dict[item[:split_pos]] = item[split_pos+1:]
  
  return Dict
  
def listMemberHelps(TargetGroup):
  """Gets help on a group's children.
  """
  Members = []
  
  for Member in TargetGroup.Config['Members'].values(): # get unique children (by discarding aliases)
    if Member not in Members:
      Members.append(Member)
    
  Ret = []
  
  for Member in Members:
    Config = Member.Config
    Ret.append(('%s%s' % (Config['name'], ', %s' % Config['alias'] if 'alias' in Config else ''), Config.get('desc', '')))
  
  return Ret
  
def isunderlying(object):
  return isinstance(object, (FunctionType, ClassType, ModuleType))
  
def isclass(object):
  return isinstance(object, ClassType)
  
def ismodule(object):
  return isinstance(object, ModuleType)
  
def isfunction(object):
  return isinstance(object, FunctionType)
