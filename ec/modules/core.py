"""
Handles the execution and the resolution of the tasks.
"""
import sys
from os import path
import traceback

from classes import Group, Task, HandledException
from helpers import err, list2dict

# State
mode = None
BaseGroup = None
is_dev_mode = None

def start(BaseModule, Argv=None, **options):
  """Starts ec.
  """
  global BaseGroup
  BaseGroup =  BaseModule.__ec_member__
  
  convertMethodsToFunctions(BaseGroup)
  
  if Argv is None:
    Argv = sys.argv[1:]
  
  global mode
  mode = 'd' if Argv else 's' # dispatch / shell mode
  
  global is_dev_mode
  is_dev_mode = options.get('dev_mode', False)
  
  if mode == 's':
    import shell
    shell.init(**options)
    
  else:
    import dispatch
    dispatch.init(Argv)
 
def execCommand(Argv, collect_missing):
  """Executes the given task with parameters.
  """
  if not Argv:
    raise HandledException('Please specify a command!')
    
  RouteParts = Argv[0].split('/')
  Args = list2dict(Argv[1:])
  
  ResolvedMember = getDescendant(BaseGroup, RouteParts[:])
  
  if not isinstance(ResolvedMember, Task):
    raise HandledException('No such task.')
    
  try:
    return ResolvedMember.__collect_n_call__(**Args) if collect_missing else ResolvedMember(**Args)
    
  except Exception as e:
    if is_dev_mode: # log the trace
      etype, value, tb = sys.exc_info()
      tb = tb.tb_next.tb_next # remove the ec - calls from the traceback, to make it more understandable
      
      message = ''.join(traceback.format_exception(etype, value, tb))[:-1]
      
    else: # provide a succinct error message
      message = str(e)
      
    raise HandledException(message)

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
    
def convertMethodsToFunctions(Target):
  """Converts all the methods of the groups to staticmethods.
  So that they could be called on the fly, without instantiation.
  """
  Underlying = Target.Underlying
  
  if isclass(Underlying): # replace existing methods of the underlying calss with staticmethods
    for attr in dir(Underlying):
      im_func = getattr(getattr(Underlying, attr), 'im_func', None)
      if im_func:
        setattr(Underlying, attr, staticmethod(im_func))
  
  for Member in Target.Config['Members'].values(): # recurse
    if not isfunction(Member.Underlying):
      convertMethodsToFunctions(Member)    
    
# Helpers
ClassType = type(Task)
def isclass(object):
  return isinstance(object, (type, ClassType))

FunctionType = type(isclass)
def isfunction(object):
  return isinstance(object, FunctionType)
