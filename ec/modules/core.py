"""
Handles the execution and the resolution of the tasks.
"""
import sys
from os import path

from classes import Group, Task, HandledException
from helpers import list2dict

# State
mode = None
BaseGroup = None

def start(BaseModule, Argv=None, **options):
  """Starts ec.
  """
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
  """Executes the given task with parameters.
  """
  RouteParts = Argv[0].split('/')
  Args = list2dict(Argv[1:])
  
  ResolvedMember = getDescendant(BaseGroup, RouteParts[:])
  
  if not isinstance(ResolvedMember, Task):
    raise HandledException('No such task.')
    
  return ResolvedMember.__collect_n_call__(**Args) if collect_missing else ResolvedMember(**Args)

def getDescendant(Ancestor, RouteParts):
  """Resolves a descendant, of the given Ancestor, as pointed by the RouteParts.
  """
  if not RouteParts:
    return Ancestor
    
  Resolved = Ancestor.Config['Members'].get(RouteParts.pop(0))
  
  if isinstance(Resolved, Group):
    return getDescendant(Resolved, RouteParts)
    
  else:
    return Resolved
    