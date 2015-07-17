import __builtin__
import shlex
from subprocess import Popen, STDOUT, PIPE

# Exports
__all__ = ['shell_exec', 'RawInputHook']

def shell_exec(command, path='.', input=''): # from gitapi.py
  proc = Popen(shlex.split(command), stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=path)
  
  out, err = [x.decode("utf-8") for x in proc.communicate(input)]
  
  return {'out': out, 'err': err, 'code': proc.returncode}
  
# Hook into existing raw_input
class RawInputHook:
  """Hooks into __builtin__.raw_input and returns the values provided by Hook.values, on by one untill the values are exhausted; then the hook is removed.
  """
  def __init__(self):
    self.origCall = __builtin__.raw_input

  def _hookOnce(self, dummy):
    value = self._values.pop(0)
    
    if not self._values: # reset the hooks
      __builtin__.raw_input = self.origCall
      
    return value
  
  def values(self, *val):
    self._values = list(val)
    __builtin__.raw_input = self._hookOnce

RawInputHook = RawInputHook()