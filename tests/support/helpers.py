import __builtin__
import shlex
from subprocess import Popen, STDOUT, PIPE

from ec.modules.classes import HandledException

# Exports
__all__ = ['shell_exec', 'RawInputHook']

def shell_exec(command, cwd='.', input=''): # from gitapi.py
  proc = Popen(shlex.split(command), stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=cwd)
  
  proc.stdin.write(input)
  out, err = [x.decode("utf-8") for x in proc.communicate()]
  
  return dict(
    out=out, err=err, code=proc.returncode,
    command=command, cwd=cwd, input=input
  )
  
# Hook into existing raw_input
class RawInputHook:
  """Hooks into __builtin__.raw_input and returns the values provided by Hook.values, on by one untill the values are exhausted; then the hook is removed.
  """
  def __init__(self):
    self.origCall = __builtin__.raw_input
    self._values = None

  def _hookOnce(self, dummy):
    value = self._values.pop(0)
    
    if not self._values: # reset the hooks
      __builtin__.raw_input = self.origCall
      
    return value
  
  def values(self, *val):
    self._values = list(val)
    __builtin__.raw_input = self._hookOnce

RawInputHook = RawInputHook()

def expect_exception(call, *ExTypes):
  """Calls the given call and excepts an exception from the given ExTypes.
  
  Args:
    *ExTypes (tuple / Exception): One or more exception types.
  """
  try:
    call()
    
  except Exception as e: #pylint: disable= W0703
    
    return isinstance(e, ExTypes)
    
shell_exec_format_string = '\ncode: {code}\nerr: {err}\nout: {out}\n--------------------\ncommand: {command}\ninput: {input}'
def checkResult(self, Result, *Vals):
  """A worker for unittest.checkResult.
  """
  for val in Vals:
    self.assertTrue(val, shell_exec_format_string.format(**Result))
  