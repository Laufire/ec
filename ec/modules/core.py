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
  BaseGroup =  BaseModule.__ec_member__
  
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
  CommandParts = Argv[0].split('/')
  Args = list2dict(Argv[1:])
  
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
    
# Sub Modules
from classes import HandledException
