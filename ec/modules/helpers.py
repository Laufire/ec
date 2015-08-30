r"""
Helpers
=======

  Generic helpers for the modules.
"""
import os
import sys
import shlex
import re
from os import path
from types import ClassType, ModuleType, FunctionType

import state

def err(message, exit_code=None):
  sys.stderr.write('%s\n' % message)

  if exit_code is not None:
    exit(exit_code)

def exit(exit_code=0):
  r"""A function to support exiting from exit hooks.

  Could also be used to exit from the calling scripts in a thread safe manner.
  """
  core.processExitHooks()

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

  path_added = False

  if not parent_path in sys.path:
    path_added = True
    sys.path.insert(0, parent_path)

  imported = __import__(name)

  if path_added:
    sys.path.pop(0)

  return imported

KWARG_VALIDATOR = re.compile('.+(?<!\\\\)=')
def getDigestableArgs(Argv):
  r"""Splits the given Argv into *Args and **KwArgs.
  """
  first_kwarg_pos = 0

  for arg in Argv:
    if KWARG_VALIDATOR.search(arg):
      break

    else:
      first_kwarg_pos += 1

  for arg in Argv[first_kwarg_pos:]: # ensure that the kwargs are valid
    if not KWARG_VALIDATOR.search(arg):
      raise HandledException('Could not parse the arg "%s".' % arg)

  return Argv[:first_kwarg_pos], list2dict(Argv[first_kwarg_pos:])

NAME_VALIDATOR = re.compile('[\\w_]+')
def validateName(name):
  assert NAME_VALIDATOR.search(name)

# mode helpers
def getMemberHelp(Target):
  if isinstance(Target, Group):
    return getGroupHelp(Target)

  elif isinstance(Target, Task):
    return getTaskHelp(Target)

def getRouteHelp(route_parts):
  Resolved = core.getDescendant(core.BaseGroup, route_parts) if route_parts else core.BaseGroup

  return getMemberHelp(Resolved)

def split(line):
  try:
    return shlex.split(line)

  except ValueError:
    raise HandledException('<command not understood>')

def getFullName(Module):
  pkg = Module.__package__

  return '%s%s' % (('%s.' % pkg) if pkg else '', Module.__name__)

# inspect helpers
def isunderlying(obj):
  return isinstance(obj, (FunctionType, ClassType, ModuleType))

def isclass(obj):
  return isinstance(obj, ClassType)

def ismodule(obj):
  return isinstance(obj, ModuleType)

def isfunction(obj):
  return isinstance(obj, FunctionType)

# Helpers
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
  r"""Gets help on a group's children.
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

def getGroupHelp(_Group):
  return '\n\n'.join([('%s:  %s' % (name, desc))[:60] for name, desc in listMemberHelps(_Group)]) # ToDo: Better formatting of the help instead of chopping the text.

def getAutoDesc(ArgConfig):
  desc = '{name}, {type_str}'.format(**ArgConfig)

  if 'default' in ArgConfig:
    desc += ' (%s)' % ArgConfig['default']

  return desc

def getTypeStr(_type):
  r"""Gets the string representation of the given type.
  """
  if isinstance(_type, CustomType):
    return _type

  if hasattr(_type, '__name__'):
    return _type.__name__

  return ''

def getTaskHelp(_Task):
  r"""Gets help on the given task member.
  """
  Ret = []

  for k in ['name', 'desc']:
    v = _Task.Config.get(k)

    if v is not None:
      Ret.append('%s: %s' % (k, v))

  Args = _Task.Args

  if Args:
    Ret.append('\nArgs:')

    for argName, Arg in Args.items():
      Ret.append('  %s: %s' % (argName, Arg.get('desc', Arg['type_str'])))

    Ret.append('')

  return '\n'.join(Ret).rstrip()

# Cross Dependencies
import core
from classes import HandledException, Group, Task, CustomType
