"""
ec
==

The main module, that allows the configuration of the importing script.
"""
from modules.helpers import get_calling_module
from modules.config import task, arg, group, module

# Exports
__all__ = [
  'start', 'call',
  'task', 'arg', 'group', 'module'
]

def start(helper_tasks=True, dev_mode=False):
  """Starts the script, if it is the main script.

  Args:
    helper_tasks (bool): Allow helper tasks ($/\*) in the shell (defaults to True).
    dev_mode (bool): Enables the logging of a detailed traceback on exceptions (defaults to False).
  """
  from modules import core
  
  CallingModule = get_calling_module()
  
  group(CallingModule) # brand the module with __ec_member__
  
  core.BaseGroup = CallingModule.__ec_member__ # allow the wrapping of ec-ed modules
  
  if CallingModule.__name__ != '__main__':
    return
  
  core.start(CallingModule, None, helper_tasks=helper_tasks, dev_mode=dev_mode)
  
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
  