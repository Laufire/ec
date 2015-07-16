"""
Handles the execution and the resolution of the tasks.
"""
import sys
from os import path
import traceback
from collections import OrderedDict

import state
from state import Settings, ModulesQ, ModuleMembers
from helpers import err, list2dict, isfunction, isclass, ismodule, isunderlying

# State
BaseGroup = None
mode = None
is_dev_mode = None

def start():
  """Starts ec.
  """
  Argv = sys.argv[1:]
  
  if not state.main_module_name in ModulesQ: # don't start the core when main is not Ec-ed
    return
    
  MainModule = sys.modules[state.main_module_name]
  
  processPendingModules()
  
  global BaseGroup
  BaseGroup =  MainModule.__ec_member__
  
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
    
  Resolved = Ancestor.Members.get(RouteParts.pop(0))
  
  if isinstance(Resolved, Group):
    return getDescendant(Resolved, RouteParts)
    
  else:
    return Resolved
    
def setActiveModule(Module):
  """Helps with collecting the members of the imported modules.
  """
  module_name = Module.__name__
  
  if module_name not in ModuleMembers:
    ModuleMembers[module_name] = []
    ModulesQ.append(module_name)
    Group(Module, {}) # brand the module with __ec_member__
  
  state.ActiveModuleMemberQ = ModuleMembers[module_name]

def resetActiveModuleToNext():
  # Remove the module name from ModulesQ as it has been processed
  ModulesQ.pop()
  
  if ModulesQ: # Set the next module's Q the ActiveModuleMemberQ, so that the configured elements could be gathered for the right target
    state.ActiveModuleMemberQ = ModuleMembers[ModulesQ[-1]]
  
def processPendingModules():
  """Processes the modules left unprocessed by the import hook.
  """
  for name in ModulesQ[:]:
    processModule(sys.modules[name])
    ModulesQ.pop()
  
def processModule(Module):
  """Builds a command tree out of the configured members of a module.
  """
  MembersTarget = []
  ClassQ = []
  Cls = None
  ClsGrpMembers = []
  
  for Member in ModuleMembers[Module.__name__]:
    
    Underlying = Member.Underlying
    member_name = Member.Config['name']
    member_alias = Member.Config.get('alias', None)
    
    if ClassQ:
      ClsGroup = ClassQ[-1]
      Cls = ClsGroup.Underlying
      
      if getattr(Cls, Underlying.__name__, None) is Underlying: # we got a member tht is a child of the previous class
        if isclass(Underlying):
          ClassQ.append(Underlying.__ec_member__)
          
        elif not isunderlying(Underlying):
          continue
          
        if member_alias:
          ClsGrpMembers.insert(0, (member_alias, Member))
          
        ClsGrpMembers.insert(0, (member_name, Member))
        continue
        
      elif Cls: # we've finished adding chidren to the previous class
        ClsGroup.Members = OrderedDict(ClsGrpMembers)
        ClsGrpMembers = []
        ClassQ.pop()
        Cls = None        
    
    if isunderlying(Underlying):
      if member_alias:
        MembersTarget.insert(0, (member_alias, Member))
        
      MembersTarget.insert(0, (member_name, Member))
      
      if isclass(Underlying):
        ClassQ.append(Underlying.__ec_member__)
        
  Module.__ec_member__.Members = OrderedDict(MembersTarget)
  
# Cross dependencies
from classes import Group, Task, HandledException
