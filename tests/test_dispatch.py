"""
Tests the.launch_ec mode.

Notes:
  * This test is used as the base by several other tests.
"""

import unittest

from support.helpers import shell_exec


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
class TestDispatch(unittest.TestCase):

  def setUp(self):
    pass

  def tearDown(self):
    pass
    
  def test_dispatch(self):
    Result = launch_ec('task1 arg1=1')
    
    assert(Result['code'] == 0)
    assert(Result['out'].strip() == '1 2')
    
  def test_multiple_args(self):
    Result = launch_ec('task1 arg1=1 arg2=1')
    
    assert(Result['code'] == 0)
    assert(Result['out'].strip() == '1 1')
    
  def test_flag_help(self):
    Result = launch_ec(flag='-h')
    
    assert(Result['code'] == 0)
    assert(Result['out'].strip()[:5] == 'Usage')
  
  def test_flag_partial(self):
    Result = launch_ec('task1 arg1=1', '1', '-p')
    
    assert(Result['code'] == 0)
    assert(Result['out'][-5:-1].strip() == '1 1')
    
  def test_absent_task(self):
    Result = launch_ec('task2')
    
    assert(Result['code'] == 1)
    assert(Result['err'].strip()[:2] == 'No')
    
  def test_nested_task(self):
    Result = launch_ec('group1/task1 arg1=1')
    
    assert(Result['code'] == 0)
    assert(Result['out'].strip() == '1')

  def test_default_arg(self):
    Result = launch_ec('task1 arg1=1')
    
    assert(Result['code'] == 0)
    assert(Result['out'].strip() == '1 2')
  
  def test_alias(self):
    Result = launch_ec('t1 arg1=1')
    
    assert(Result['code'] == 0)
    assert(Result['out'].strip() == '1 2')
  
if __name__ == '__main__':
  unittest.main()
