import sys
import imp
from os import path

from modules.classes import Group, Task

# State
mode = None
BaseGroup = {}

def start():
  argv = sys.argv[1:]
  
  if not argv:
    show_usage()
    return
  
  extendBuiltins()
  
  Body = load_module(argv.pop(0))
  
  global BaseGroup
  BaseGroup = Group(Body)
  
  global mode
  mode = 'd' if argv else 's' # dispatch / shell mode
  
  if mode == 's':
    import shell
    shell.init()
    
  else:
    import dispatch
    dispatch.init(argv)
 
def exec_command(Argv, collect_missing):
  CommandParts, Args = split_input(Argv)
  ResolvedMember = resolveMember(BaseGroup, CommandParts[:])
  
  if not isinstance(ResolvedMember, Task):
    raise HandledException('No such task.')
    
  return ResolvedMember.collectNcall(**Args) if collect_missing else ResolvedMember(**Args)

# Helpers 
def show_usage():
  print 'private module_path <command route> [options]'
  
def load_module(module_path):
  module_path = path.abspath(module_path)
  parent_path, name = path.split(module_path)
  name, dummy = path.splitext(name)
  
  sys.path.insert(0, parent_path)
  Module = imp.load_source(name, module_path)
  
  return Module

def extendBuiltins(): # add the methods used by the scripts to __builtins__
  import decorators
  
  for item in decorators.__all__:
    __builtins__[item] = getattr(decorators, item)
    
def split_input(argv):
  arg_start = 0
  count = len(argv)
  
  while arg_start < count:
    if argv[arg_start].find('=') > -1:
      break
    
    arg_start += 1
    
  CommandParts = argv[:arg_start]
  Args = {}
  
  for arg in argv[arg_start:]:
    split_pos = arg.find('=')
    Args[arg[:split_pos]] = arg[split_pos+1:]
  
  return CommandParts, Args
  
def resolveMember(Parent, CommandParts):
  
  if not CommandParts:
    return Parent
    
  Resolved = Parent.Config['Members'].get(CommandParts.pop(0))
  
  if isinstance(Resolved, Group):
    return resolveMember(Resolved, CommandParts)
    
  else:
    return Resolved
    
# Sub Modules
from classes import HandledException
