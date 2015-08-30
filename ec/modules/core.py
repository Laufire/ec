r"""
Handles the execution and the resolution of the tasks.
"""
import sys
import traceback
from collections import OrderedDict

import state
from state import Settings, ModulesQ, ModuleMembers, ExitHooks
from helpers import getDigestableArgs, isclass, isunderlying

# State
BaseGroup = None
mode = None
is_dev_mode = None

def start():
  r"""Starts ec.
  """
  processPendingModules()

  if not state.main_module_name in ModuleMembers: # don't start the core when main is not Ec-ed
    return

  MainModule = sys.modules[state.main_module_name]

  if not MainModule.__ec_member__.Members: # there was some error while loading script(s)
    return

  global BaseGroup
  BaseGroup = MainModule.__ec_member__

  Argv = sys.argv[1:]
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

  processExitHooks()

def execCommand(Argv, collect_missing):
  r"""Executes the given task with parameters.
  """
  try:
    return _execCommand(Argv, collect_missing)

  except Exception as e:
    if is_dev_mode: # log the trace
      etype, value, tb = sys.exc_info()
      tb = tb.tb_next.tb_next # remove the ec - calls from the traceback, to make it more understandable

      message = ''.join(traceback.format_exception(etype, value, tb))[:-1]

    else:
      if isinstance(e, HandledException): # let the modes handle the HandledException
        raise e

      message = str(e) # provide a succinct error message

    raise HandledException(message)

def getDescendant(Ancestor, RouteParts):
  r"""Resolves a descendant, of the given Ancestor, as pointed by the RouteParts.
  """
  if not RouteParts:
    return Ancestor

  Resolved = Ancestor.Members.get(RouteParts.pop(0))

  if isinstance(Resolved, Group):
    return getDescendant(Resolved, RouteParts)

  else:
    return Resolved

def setActiveModule(Module):
  r"""Helps with collecting the members of the imported modules.
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
  r"""Processes the modules left unprocessed by the import hook.
  """
  for name in ModulesQ[:]:
    processModule(name)
    ModulesQ.pop()

def processModule(module_name):
  r"""Builds a command tree out of the configured members of a module.
  """
  Module = sys.modules[module_name]
  MembersTarget = []
  ClassQ = []
  Cls = None
  ClsGroup = None
  ClsGrpMembers = []

  for Member in ModuleMembers[module_name]:
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

      elif Cls: # we've finished adding children to the previous class
        ClsGroup.Members = OrderedDict(ClsGrpMembers)
        ClsGrpMembers = []
        ClassQ.pop()
        Cls = None
        ClsGroup = None

    if isunderlying(Underlying):
      if member_alias:
        MembersTarget.insert(0, (member_alias, Member))

      MembersTarget.insert(0, (member_name, Member))

      if isclass(Underlying):
        ClassQ.append(Underlying.__ec_member__)

  if ClsGroup:
    ClsGroup.Members = OrderedDict(ClsGrpMembers)

  ModuleMembers[module_name] = []  # remove the existing members from the cache so that they won't be processed again

  if not hasattr(Module.__ec_member__, 'Members'):
    Module.__ec_member__.Members = OrderedDict(MembersTarget)

def processExitHooks():
  for hook in ExitHooks:
    hook()

# Helpers
def _execCommand(Argv, collect_missing):
  r"""Worker of execCommand.
  """
  if not Argv:
    raise HandledException('Please specify a command!')

  RouteParts = Argv[0].split('/')
  Args, KwArgs = getDigestableArgs(Argv[1:])

  ResolvedMember = getDescendant(BaseGroup, RouteParts[:])

  if isinstance(ResolvedMember, Group):
    raise HandledException('Please specify a task.', Member=ResolvedMember)

  if not isinstance(ResolvedMember, Task):
    raise HandledException('No such task.', Member=BaseGroup)

  return ResolvedMember.__collect_n_call__(*Args, **KwArgs) if collect_missing else ResolvedMember(*Args, **KwArgs)

# Cross dependencies
from classes import Group, Task, HandledException
