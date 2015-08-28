r"""
ec
==

The main module, that allows the configuration of the importing script.
"""
import sys

from modules.state import Settings, ModulesQ
from modules.helpers import getCallingModule
from modules.config import task, arg, group, module, member, exit_hook
from modules import hooks

# Exports
__all__ = [
  'task', 'arg', 'group', 'module', 'member', 'exit_hook',
  'settings', 'call',
]

def settings(**NewSettings):
  r"""Sets the settings of ec.

  Settings:
    * helper_tasks (bool): Allow helper tasks ($/\*) in the shell (defaults to True).
    * dev_mode (bool): Enables the logging of a detailed traceback on exceptions (defaults to False).
    * clean (bool): cleans the existing settings before applying new settings.
  """

  if 'clean' in Settings:
    Settings.clear()

  Settings.update(**NewSettings)

def call(__ec_func__, *Args, **KwArgs):
  r"""Helps with calling the tasks with partial arguments (within the script being configured).

  The unavailable args will be collected before calling the function.

  Args:
    __ec_func__: A function that has been configured for ec.
    \*Args: Partial args for the function.
    \*\*KwArgs: Partial kwargs for the function.

  Notes:
    * The param name **__ec_func__** is chosen, in order to avoid collision with the **KwArgs**.
  """
  return __ec_func__.__ec_member__.__collect_n_call__(*Args, **KwArgs)

# Main
hooks.EcModuleName = __name__

FirstCaller = getCallingModule()

def registerFirstCaller(): # Note: the FirstCaller should be registered separately as the import wouldn't be hooked yet.
  from modules import core

  core.setActiveModule(FirstCaller)

def main():
  from modules.hooks import isImportHooked, registerExitCall, hookIntoImport

  registerExitCall()

  if not isImportHooked():
    hookIntoImport()
    registerFirstCaller()

main()
