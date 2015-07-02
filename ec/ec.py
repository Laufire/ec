# -*- coding: utf-8 -*-
"""
ec
===
"""

__version__ = '0.1.0'

from modules.helpers import get_calling_module
from modules.config import task, arg, group, module

# Exports
__all__ = [
  'start', 'call',
  'task', 'arg', 'group', 'module'
]

def start(helper_tasks=True):
  """Starts the script, if it is the main script.

  :param helper_tasks: enables / disables helper tasks ($ ..) in the shell.
  :param helper_tasks: default True
  """
  from modules import core
  
  CallingModule = get_calling_module()
  
  group(CallingModule) # brand the module with __ec_member__
  
  core.BaseGroup = CallingModule.__ec_member__ # allow the wrapping of ec-ed modules
  
  if CallingModule.__name__ != '__main__':
    return
  
  core.start(CallingModule, None, helper_tasks=helper_tasks)
  
def call(__ec_func__, **InArgs):
  """Helps with calling the tasks with partial arguments.
    The unavailable args will be collected before calling the function.
  """
  return __ec_func__.__ec_member__.__collect_n_call__(**InArgs)
  