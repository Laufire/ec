"""
interface
=========

Allows the importing of ec, as a module.
"""
import shlex

from modules import core
from modules.core import _execCommand, getDescendant, processPendingModules
from modules import hooks
from modules.state import ModuleMembers
from modules.classes import Task, Group, HandledException
from modules.helpers import getCallingModule, isfunction

__all__ = ['setBase', 'resolve', 'call', 'force_config', 'add']

# Exports
def setBase(Underlying):
  """Sets the base for the interface to work on.
  
  Args:
    Underlying (Group): The Group set as the base, from which all the commands are resolved.
  """
  core.processPendingModules()
  core.BaseGroup = Underlying.__ec_member__

def resolve(route):
  """Resolves the member identified by the route.
  
  Args:
    route (str): The route route to resolve. **Ex:** *group1/task1*.
    
  Returns:
    A Member, if the resolves one, or None if it doesn't.
  """
  return getDescendant(core.BaseGroup, shlex.split(route))
  
def call(command, collect_missing=False):
  """Calls a task, as if it were called from the command line.
  
  Args:
    command (str): A route followed by params (as if it were entered in the shell).
    collect_missing (bool): Collects any missing argument for the command through the shell. Defaults to False.
    
  Returns:
    The return value of the called command.
  """
  return _execCommand(shlex.split(command), collect_missing)
  
  
def force_config():
  """Forces the configuration of the members of the calling module. So that the configured members would be available for manipulation.
  
  Note:
    A call to this function will only be necessary when modifying an ec script witihin itself, as scripts are implicitly configured after their import.
  """
  core.processModule(getCallingModule().__name__)
  

def add(TargetGroup, NewMember, Config=None, Args=None):
  """Adds members to an existing group.
  
  Args:
    TargetGroup (Group): The target group for the addition.
    NewMember (Group / Task): The member to be added.
    Config (dict): The config for the member.
    Args (OrderedDict): ArgConfig for the NewMember, if it's a task (optional).
  """
  Member = Task(NewMember, Args or {}, Config or {}) if isfunction(NewMember) else Group(NewMember, Config or {})
  ParentMembers = TargetGroup.__ec_member__.Members
  
  ParentMembers[Member.Config['name']] = Member
  
  alias = Member.Config.get('alias')
  if alias:
    ParentMembers[alias] = Member
  
# main
if not hooks.isImportHooked():
  hooks.EcModuleName = '%s.ec' % __name__[:__name__.rfind('.')]
  hooks.hookIntoImport()
  