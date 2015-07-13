"""
Tests the dispatch mode.

Notes:
  * This test is used as the base by several other tests.
"""

import unittest

from support.helpers import shell_exec

# Overridables - could be overridden by other tests.
script_name = 'support/target_script.py'
command_prefix = ''

def dispatch(argStr='', input='', flag=''):
  return shell_exec('python tests/%s %s%s%s' % (script_name, flag, command_prefix if flag != '-h' else '', argStr), input=input)
  
# Tests
class TestDispatch(unittest.TestCase):

  def setUp(self):
    pass

  def tearDown(self):
    pass
    
  def test_dispatch(self):
    Result = dispatch('task1 arg1=1')
    
    assert(Result['code'] == 0)
    assert(Result['out'].strip() == '1 2')
    
  def test_multiple_args(self):
    Result = dispatch('task1 arg1=1 arg2=1')
    
    assert(Result['code'] == 0)
    assert(Result['out'].strip() == '1 1')
    
  def test_flag_help(self):
    Result = dispatch(flag='-h')
    
    assert(Result['code'] == 0)
    assert(Result['out'].strip()[:5] == 'Usage')
  
  def test_flag_partial(self):
    Result = dispatch('task1 arg1=1', '1', '-p ')
    
    assert(Result['code'] == 0)
    assert(Result['out'][-5:-1].strip() == '1 1')
    
  def test_absent_task(self):
    Result = dispatch('task2')
    
    assert(Result['code'] == 1)
    assert(Result['err'].strip()[:2] == 'No')
    
  def test_nested_task(self):
    Result = dispatch('group1/task1 arg1=1')
    
    assert(Result['code'] == 0)
    assert(Result['out'].strip() == '1')

  def test_default_arg(self):
    Result = dispatch('task1 arg1=1')
    
    assert(Result['code'] == 0)
    assert(Result['out'].strip() == '1 2')
  
  def test_alias(self):
    Result = dispatch('t1 arg1=1')
    
    assert(Result['code'] == 0)
    assert(Result['out'].strip() == '1 2')
  
if __name__ == '__main__':
  unittest.main()
