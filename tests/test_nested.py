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
  """Dispatches command to the target script.
  """
  if flag == '-h':
    rest = flag
    
  elif flag == '-p':
    
    rest = '%s target_script/%s' % (flag, argStr)
    
  else:
    
    rest = 'target_script/%s' % argStr
    
  return shell_exec('python tests/support/nester.py %s' % rest, input=input)
    

test_dispatch.launch_ec = launch_ec

TestNested = test_dispatch.TestDispatch

if __name__ == '__main__':
  unittest.main()
