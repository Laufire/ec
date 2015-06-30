# -*- coding: utf-8 -*-
"""
private
========
"""

__version__ = '0.1.0'

from modules.helpers import get_calling_module
from modules.config import task, arg, group, module

# Exports
__all__ = ['start', 'task', 'arg', 'group', 'module']

def start():
  """Start
  """
  CallingModule = get_calling_module()
  
  group(CallingModule) # brand the module with __pr_member__
  
  if CallingModule.__name__ != '__main__':
    return
  
  from modules import core
  core.start(CallingModule)