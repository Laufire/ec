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
  """Dispatches command to a nested script.
  """
  command = 'python tests/support/nester.py'
    
  if flag:
    command += ' %s' % flag
    
  if argStr:
    
    command += ' target_script/%s' % argStr
    
  return shell_exec(command, input=input)

test_dispatch.launch_ec = launch_ec

TestNested = test_dispatch.TestDispatch

if __name__ == '__main__':
  unittest.main()
