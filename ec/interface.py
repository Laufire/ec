"""
interface
=========

Allows the importing of ec, as a module.
"""
import shlex

from modules import core
from modules.core import execCommand, getDescendant, processPendingModules
from modules import hooks

__all__ = ['setBase', 'resolve', 'call']

# Exports
def setBase(Underlying):
  """Sets the base for the interface to work on.
  """
  from modules import state
  
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
    
  Returns:
    The return value of the called command.
  """
  return execCommand(shlex.split(command), collect_missing)
  
# main
if hooks.isImportHooked(): # import hooks has been added by ec.FirstCaller, hence it wouldn't be processed automatically
  processPendingModules()
  
else:
  hooks.EcModuleName = '%s.ec' % __name__[:__name__.rfind('.')]
  hooks.hookIntoImport()
  