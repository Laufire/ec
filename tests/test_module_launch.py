"""
Tests nested scripts.

Note:
  The test cases for this test are provided by test_dispatch.
"""

import unittest

from support.helpers import shell_exec

# Modifications to test_dispatch
import test_dispatch

def launch_ec(argStr='', input='', flag=''):
  """Dispatches command to ec (loaded as a module).
  """  
  command = 'python -m ec tests/support/target_script.py'
  
  if flag:
    command += ' %s' % flag
    
  if argStr:
    
    command += ' %s' % argStr
    
  return shell_exec(command, input=input)

test_dispatch.launch_ec = launch_ec

TestEntryPointLaunch = test_dispatch.TestDispatch

if __name__ == '__main__':
  unittest.main()
