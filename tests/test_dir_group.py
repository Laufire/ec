"""
Tests dir group (launching dirs with all the ec based modules as groups).

Note:
  The test cases for this test are provided by test_dispatch.
"""

import unittest

from support.helpers import shell_exec

def launch_ec(argStr='', input='', flag=''):
  """Launches the support dir.
  """
  command = 'ec tests/support'
    
  if flag:
    command += ' %s' % flag
    
  if argStr:
    
    command += ' target_script/%s' % argStr
    
  return shell_exec(command, input=input)


import test_dispatch # The test cases are imported from test_dispatch

test_dispatch.launch_ec = launch_ec # replace the.launch_ec function of test_dispatch

TestDirGroup = test_dispatch.TestDispatch # assign the test to a variable so that unittest could find it

class TestDirGroupOnLaunchers(unittest.TestCase):

  def setUp(self):
    pass

  def tearDown(self):
    pass
    
  def test_entry_point_launch(self):
    Result = shell_exec('ec tests/support target_script/task1 arg1=1')
    
    assert(Result['code'] == 0)
    assert(Result['out'].strip() == '1 2')
    
  def test_module_launch(self):
    Result = shell_exec('python -m ec tests/support target_script/task1 arg1=1')
    
    assert(Result['code'] == 0)
    assert(Result['out'].strip() == '1 2')

if __name__ == '__main__':
  unittest.main()
