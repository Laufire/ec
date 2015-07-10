"""
Tests dir group (launching dirs with all the ec based modules as groups).

Note:
  The test cases for this test are provided by test_dispatch.
"""

import unittest

from support.helpers import shell_exec

def dispatch(argStr, input=''):
  """Launches the support dir."""
  
  flag = argStr[:2]
  
  if flag == '-h':
    command = 'ec tests/support %s' % argStr
    
  elif flag == '-p':
    
    command = 'ec tests/support -p target_script/%s' % argStr[3:]
    
  else:
    
    command = 'ec tests/support target_script/%s' % argStr
    
  return shell_exec(command, input=input)


import test_dispatch # The test cases are imported from test_dispatch

test_dispatch.dispatch = dispatch # replace the dispatch function of test_dispatch

TestDirGroup = test_dispatch.TestDispatch # assign the test to a variable so that unittest could find it

if __name__ == '__main__':
  unittest.main()
