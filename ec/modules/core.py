"""
Handles the execution and the resolution of the tasks.
"""
import sys
from os import path
import traceback
from collections import OrderedDict

import state
from state import Settings, ModulesQ
from helpers import err, list2dict, isfunction, isclass, ismodule, isunderlying

# State
BaseGroup = None
mode = None
is_dev_mode = None

def start(BaseModule, Argv=None):
  """Starts ec.
  """
  if Argv is None:
    Argv = sys.argv[1:]
  
  processModule(BaseModule)
  global BaseGroup
  BaseGroup =  BaseModule.__ec_member__
  
  global mode
  mode = 'd' if Argv else 's' # dispatch / shell mode
  
  global is_dev_mode
  is_dev_mode = Settings.get('dev_mode', False)
  
  if mode == 's':
    import shell
    shell.init()
    
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
    
def processModule(Module):
  """Builds a command tree out of the configured members of a module.
  """
  MembersTarget = []
  ClassQ = []
  Cls = None
  
  for Member in ModulesQ[-1]:
    Underlying = Member.Underlying
    member_name = Member.Config['name']
    member_alias = Member.Config.get('alias', None)
    
    if ClassQ:
      ClsGroup = ClassQ[-1]
      Cls = ClsGroup.Underlying
      ClsMembersTarget = ClsGroup.Config.get('Members', [])
      underlying_name = Underlying.__name__
      CurrentMember = getattr(Cls, underlying_name, None) # Note: The methods of classes would be different than the functions registerd by @task
      
      if  CurrentMember and getattr(CurrentMember, 'im_func', Underlying) is Underlying:
      
        if isfunction(Underlying):
          im_func = CurrentMember.im_func # convert the method into a function so it could be used within the script like object methods (without a refrence to self)
          setattr(Cls, underlying_name, im_func)
          im_func.__ec_member__ = Member
          Member.Underlying = im_func
          
        elif isclass(Underlying):
          ClassQ.append(Underlying.__ec_member__)
          
        elif not ismodule(Underlying):
          continue
          
        if member_alias:
          ClsMembersTarget.insert(0, (member_alias, Member))
          
        ClsMembersTarget.insert(0, (member_name, Member))
        ClsGroup.Config['Members'] = ClsMembersTarget
        continue
        
      else:
      
        if Cls:
          ClsGroup.Config['Members'] = OrderedDict(ClsGroup.Config['Members'])
          ClassQ.pop()
          convertNonEcMethodsToStatic(Cls)
          Cls = None        
    
    if isunderlying(Underlying):
      if member_alias:
        MembersTarget.insert(0, (member_alias, Member))
        
      MembersTarget.insert(0, (member_name, Member))
      
      if isclass(Underlying):
        ClassQ.append(Underlying.__ec_member__)
        
  if Cls:
    convertNonEcMethodsToStatic(Cls)
  
  # Brand the module with __ec_member__
  __ec_member__ = getattr(Module, '__ec_member__', None)
  if not __ec_member__:
    __ec_member__ = Group(Module, {})
  
  __ec_member__.Config['Members'] = OrderedDict(MembersTarget)
  
def convertNonEcMethodsToStatic(Cls):
  """Convert helper methods of a Group into statics, so that they too could be called like group.helper(...) like the tasks of the group.
  """
  for attr in dir(Cls):
    im_func = getattr(getattr(Cls, attr), 'im_func', None)
    if im_func and not hasattr(im_func, '__ec_member__'):
      setattr(Cls, attr, staticmethod(im_func))
  
# Cross dependencies
from classes import Group, Task, HandledException
