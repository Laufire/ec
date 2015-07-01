# -*- coding: utf-8 -*-
"""
private
========
"""

__version__ = '0.1.0'

from modules.helpers import get_calling_module
from modules.config import task, arg, group, module

# Exports
__all__ = [
  'start', 'call',
  'task', 'arg', 'group', 'module'
]

def start():
  """Starts the script, if it is the main script.
  """
  CallingModule = get_calling_module()
  
  group(CallingModule) # brand the module with __pr_member__
  
  if CallingModule.__name__ != '__main__':
    return
  
  from modules import core
  core.start(CallingModule)
  
def call(__pr_func__, **InArgs):
  """Helps with calling the tasks with partial arguments.
    The unavailable args will be collected before calling the function.
  """
  return __pr_func__.__pr_member__.__collect_n_call__(**InArgs)
  