"""
The global state for ec.

  Stores the gobal variables stored across modules.
  
  Note:
    The module should not depend on other modules, in order to avoid cross dependency issues.
"""

from collections import OrderedDict

Settings = {}

main_module_name = '__main__'

ModulesQ = []

ActiveModuleMemberQ = None # used to collect the configured members of the current module

ModuleMembers = {}
