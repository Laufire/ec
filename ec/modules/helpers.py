"""
Helpers

  Generic helpers for the modules.
"""
import os
import sys
import shlex
from os import path
from types import ClassType, ModuleType, FunctionType

import state

def err(message, exit_code=None):
  sys.stderr.write('%s\n' % message)
  
  if exit_code is not None:
    exit(exit_code)

def exit(exit_code=0):
  """A function to support eiting from exit hooks.
  """
  if state.isExitHooked and not hasattr(sys, 'exitfunc'): # the function is called from the exit hook
    sys.stderr.flush()
    sys.stdout.flush()
    os._exit(exit_code) #pylint: disable=W0212
    
  sys.exit(exit_code)
  
def getCallingModule():
  return sys.modules[sys._getframe().f_back.f_back.f_globals['__name__']] #pylint: disable=W0212

def load_module(module_path):
  module_path = path.abspath(module_path)
  parent_path, name = path.split(module_path)
  name, dummy = path.splitext(name)
  
  sys.path.insert(0, parent_path)
  imported = __import__(name)
  sys.path.pop(0)
  
  return imported

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
  
  for Member in TargetGroup.Members.values(): # get unique children (by discarding aliases)
    if Member not in Members:
      Members.append(Member)
    
  Ret = []
  
  for Member in Members:
    Config = Member.Config
    Ret.append(('%s%s' % (Config['name'], ', %s' % Config['alias'] if 'alias' in Config else ''), Config.get('desc', '')))
  
  return Ret
  
def split(line):
  try:
    return shlex.split(line)
    
  except ValueError:
    raise HandledException('<command not understood>')
    
def getFullName(Module):
  pkg = Module.__package__
  
  return '%s%s' % (('%s.' % pkg) if pkg else '', Module.__name__)
  
# inspect helpers
def isunderlying(object):
  return isinstance(object, (FunctionType, ClassType, ModuleType))
  
def isclass(object):
  return isinstance(object, ClassType)
  
def ismodule(object):
  return isinstance(object, ModuleType)
  
def isfunction(object):
  return isinstance(object, FunctionType)

# Cross Dependencies
from classes import HandledException
