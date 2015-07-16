import __builtin__

import state
from state import ModulesQ, ModuleMembers
from helpers import getCallingModule
import core

# State
isExitHooked = False
EcModuleName = None # would be set by ec.ec
origImp = __builtin__.__import__

# Exports
def isImportHooked():
  return __builtin__.__import__ != origImp

def hookIntoImport():
  if isImportHooked():
    return
  
  # hook into __import__ to register modules when they import ec.
  def newImp(name, *rest):
    if name == EcModuleName:
      core.setActiveModule(getCallingModule())
      
      return origImp(name, *rest)
    
    else:
      imported = origImp(name, *rest)
      
      if imported.__name__ in ModulesQ:
        core.processModule(imported)
        core.resetActiveModuleToNext()
        
      return imported

  __builtin__.__import__ = newImp

def registerExitCall():
  """Registers an exit call to start the core.
  
    The core would be started after the main module is loaded. Ec would be exited from the core.
  """
  global isExitHooked
  
  if isExitHooked:
    return
    
  isExitHooked = True
  
  from atexit import register
  
  register(core.start) # start the core when the main module exits
  