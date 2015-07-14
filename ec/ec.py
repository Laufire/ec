"""
ec
==

The main module, that allows the configuration of the importing script.
"""
import sys

from modules.state import Settings, ECedModules, ModulesQ
from modules.helpers import getCallingModule
from modules.config import task, arg, group, module, member
from modules import core

# Exports
__all__ = [
  'settings', 'call',
  'task', 'arg', 'group', 'module', 'member'
]

def settings(**NewSettings):
  """Sets the settings of ec.
  
  Settings:
    * helper_tasks (bool): Allow helper tasks ($/\*) in the shell (defaults to True).
    * dev_mode (bool): Enables the logging of a detailed traceback on exceptions (defaults to False).
    * clean (bool): cleans the existing settings before applying new settings.
  """
  
  if 'clean' in Settings:
    Settings.clear()
    
  Settings.update(**NewSettings)
  
def call(__ec_func__, **Args):
  """Helps with calling the tasks with partial arguments (within the script being configured).
  
  The unavailable args will be collected before calling the function.
  
  Args:
    __ec_func__: A function that has been configured for ec.
    **Args: Partial args for the function.
    
  Notes:
    * The param name **__ec_func__** is chosen, in order to avoid collision with the **Args**.
  """
  return __ec_func__.__ec_member__.__collect_n_call__(**Args)

  
# Main
Caller = getCallingModule()

def register_exit_call():
  """Register an exit call to start the core.
  
    The core would be started after the main module is loaded. Ec would be exited from the core.
  """
  import atexit
  
  @atexit.register
  def exit_hook():
    core.start(Caller)

def hook_into_import():
  # hook into __import__ to register modules when they import ec
  import __builtin__
  
  origImp = __builtin__.__import__
  
  def newImp(name, *x):
    if name in ECedModules:
      return origImp(name, *x)
      
    if name == __name__:
      ECedModules.add(getCallingModule().__name__)
      
      return origImp(name, *x)
    
    else:
      ModulesQ.append([])
      
      imported = origImp(name, *x)
      
      if imported.__name__ in ECedModules:
        core.processModule(imported)
      
      ModulesQ.pop()
      return imported

  __builtin__.__import__ = newImp

def main():
  register_exit_call()
  hook_into_import()
  
main()
