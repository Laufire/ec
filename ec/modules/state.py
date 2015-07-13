"""
The global state for ec.

  Stores the gobal variables stored across modules.
  
  Note:
    The module should not depend on other modules, in order to avoid cross dependency issues.
"""

from collections import OrderedDict

Settings = {}

ModuleMembers = OrderedDict() # Stores the module members for organising

ModulesQ = [] # Stores the module members for organising