import __builtin__

import state
from state import ModulesQ, ModuleMembers
from helpers import getCallingModule, getFullName
import core

# State
EcModuleName = None # would be set by ec.ec
origImp = __builtin__.__import__

# Exports
def isImportHooked():
  return __builtin__.__import__ != origImp

def hookIntoImport():
  if isImportHooked():
    return
  
  def getModuleFullName(Module, globals):
    
    module_name = Module.__name__
    
    if '.' in module_name:
      return module_name
      
    if not globals:
      return module_name
      
    pkg_name = globals.get("__name__")
    
    if not pkg_name:
      return module_name
      
    if globals.has_key("__path__"):
      return '%s.%s' % (pkg_name, module_name)
      
    last_dot_pos = pkg_name.rfind('.')
    
    if last_dot_pos > -1:
      return '%s.%s' % (pkg_name[:last_dot_pos], module_name)
      
    return module_name

  # hook into __import__ to register modules when they import ec.
  def newImp(name, globals=None, *rest, **kwargs):
    if name == EcModuleName:
      core.setActiveModule(getCallingModule())
      
      return origImp(name, globals, *rest, **kwargs)
    
    else:
      imported = origImp(name, globals, *rest, **kwargs)
      
      module_name = getModuleFullName(imported, globals)
      if module_name in ModulesQ:
        core.processModule(imported)
        core.resetActiveModuleToNext()
        
      return imported

  __builtin__.__import__ = newImp

def registerExitCall():
  """Registers an exit call to start the core.
  
    The core would be started after the main module is loaded. Ec would be exited from the core.
  """
  if state.isExitHooked:
    return
    
  state.isExitHooked = True
  
  from atexit import register
  
  register(core.start) # start the core when the main module exits
  