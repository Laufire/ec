import sys
from os import path

from classes import Group, Task
from helpers import list2dict

# State
mode = None
BaseGroup = None

# Exports
__all__ = ['start', 'execCommand', 'resolveMember']

def start(BaseModule, Argv=None, **options):
  global BaseGroup
  BaseGroup =  BaseModule.__pr_member__
  
  if Argv is None:
    Argv = sys.argv[1:]
  
  global mode
  mode = 'd' if Argv else 's' # dispatch / shell mode
  
  if mode == 's':
    import shell
    shell.init(**options)
    
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
  Args = list2dict(argv[arg_start:])
  
  return CommandParts, Args
  
# Sub Modules
from classes import HandledException
