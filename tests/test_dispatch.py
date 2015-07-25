"""
Tests the dispatch mode.

Notes:
  * This test is used as the base by several other tests.
"""

import unittest

from support.helpers import shell_exec

def launch_ec(argStr='', input='', flag=''):
  """Dispatches command to the target script.
  """  
  command = 'python tests/support/target_script.py'
  
  if flag:
    command += ' %s' % flag
    
  if argStr:
    
    command += ' %s' % argStr
    
  return shell_exec(command, input=input)
    
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
    
  def test_positional_args(self):
    Result = launch_ec('task1 1')
    
    assert(Result['code'] == 0)
    assert(Result['out'].strip() == '1 2')
    
  def test_mixed_args(self):
    Result = launch_ec('task1 1 arg2=1')
    
    assert(Result['code'] == 0)
    assert(Result['out'].strip() == '1 1')
    
  def test_flag_help(self):
    Result = launch_ec(flag='-h')
    
    assert(Result['code'] == 0)
    assert(Result['out'].strip()[:5] == 'Usage')
    
  def test_flag_help_task(self):
    Result = launch_ec(flag='-h', argStr='task1')
    
    assert(Result['code'] == 0)
    assert(Result['out'].find('Args:') > -1)
  
  def test_flag_help_group(self):
    Result = launch_ec(flag='-h', argStr='group1')
    
    assert(Result['code'] == 0)
    assert(Result['out'].find('task1') > -1)
  
  def test_flag_help_subgroup(self):
    Result = launch_ec(flag='-h', argStr='group1/task1')
    
    assert(Result['code'] == 0)
    assert(Result['out'].find('Args:') > -1)
  
  def test_flag_partial(self):
    Result = launch_ec('task1 arg1=1', '1', '-p')
    
    assert(Result['code'] == 0)
    assert(Result['out'][-5:-1].strip() == '1 1')
    
  def test_absent_task(self):
    Result = launch_ec('task2')
    
    assert(Result['code'] == 1)
    assert(Result['err'].strip()[:2] == 'No')
    assert(Result['err'].find('Members') > -1) # check whether a help string is presented
    
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
    
  def test_handled_exception(self):
    Result = launch_ec('hex')
    
    assert(Result['code'] == 1)
    assert(Result['err'].find('Invalid') > -1)
    assert(Result['err'].find('arg1') > -1)
    assert(Result['err'].find('int') > -1)
    assert(Result['err'].find('got') > -1)
    
  def test_exception(self):
    Result = launch_ec('ex')
    
    assert(Result['code'] == 1)
    assert(Result['err'].strip() == 'integer division or modulo by zero')
  
if __name__ == '__main__':
  unittest.main()
