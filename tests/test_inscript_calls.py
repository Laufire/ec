"""
Tests the.launch_ec mode.

Notes:
  * This test is used as the base by several other tests.
"""

import unittest

from support.helpers import shell_exec

from support.target_script import task1, group1

def launch_ec(argStr='', input='', flag=''):
  """Dispatches command to the target script."""
  
  if flag == '-h':
    rest = flag
    
  elif flag == '-p':
    
    rest = '%s %s' % (flag, argStr)
    
  else:
    
    rest = argStr
    
  return shell_exec('python tests/support/target_script.py %s' % rest, input=input)
    
# Tests
class TestInscriptCalls(unittest.TestCase):

  def setUp(self):
    pass

  def tearDown(self):
    pass
    
  def test_task_call(self):
    assert(task1(1) == (1, 2))
    
  def test_group_task_call(self):
    assert(group1.task1(1) == 1)
  
if __name__ == '__main__':
  unittest.main()
