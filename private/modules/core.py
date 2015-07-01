import sys
from os import path

from classes import Group, Task

# State
mode = None
BaseGroup = {}

# Exports
__all__ = ['start', 'execCommand', ]

def start(BaseModule, Argv=None):
  global BaseGroup
  BaseGroup =  BaseModule.__pr_member__
  
  if Argv is None:
    Argv = sys.argv[1:]
  
  global mode
  mode = 'd' if Argv else 's' # dispatch / shell mode
  
  if mode == 's':
    import shell
    shell.init()
    
  else:
    import dispatch
    dispatch.init(Argv)
 
def execCommand(Argv, collect_missing):
  CommandParts, Args = _split_input(Argv)
  
  ResolvedMember = resolveMember(BaseGroup, CommandParts[:])
  
  if not isinstance(ResolvedMember, Task):
    raise HandledException('No such task.')
    
  return ResolvedMember.__collect_n_call__(**Args) if collect_missing else ResolvedMember(**Args)

def resolveMember(Parent, CommandParts):
  
  if not CommandParts:
    return Parent
    
  Resolved = Parent.Config['Members'].get(CommandParts.pop(0))
  
  if isinstance(Resolved, Group):
    return resolveMember(Resolved, CommandParts)
    
  else:
    return Resolved
    
# Helpers
def _split_input(argv):
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
  
# Sub Modules
from classes import HandledException
