"""
Tests the shell mode.
"""

import unittest

from support.helpers import shell_exec


def launch_ec(*lines):
  """Passes commands through the shell.
  """
  return shell_exec('python tests/support/target_script.py', input='%s\n\0' % '\r\n'.join(lines))

class TestShell(unittest.TestCase):

  def setUp(self):
    pass

  def tearDown(self):
    pass
    
  def test_task(self):
    Result = launch_ec('task1', '1', '2', '3')
    
    assert(Result['code'] == 0)
    assert(Result['out'].find('(1, 2)') > -1)
    
  def test_multiple_args(self):
    Result = launch_ec('task1 arg1=1 arg2=1')
    
    assert(Result['code'] == 0)
    assert(Result['out'].find('(1, 1)') > -1)
    
  def test_help(self):
    Result = launch_ec('h', '')
    assert(Result['code'] == 0)
    
    out = Result['out']    
    assert(out.find('task1') > -1)
    assert(out.find('group1') > -1)
    assert(out.find('task1') > -1)
  
  def test_absent_task(self):
    Result = launch_ec('task2')
    
    assert(Result['code'] == 0)
    assert(Result['err'].strip()[:2] == 'No')
    
  def test_nested_task(self):
    Result = launch_ec('group1/task1 arg1=100000')
    
    assert(Result['code'] == 0)
    assert(Result['out'].find('100000') > -1)

  def test_default_arg(self):
    Result = launch_ec('task1 arg1=1', '')
    
    assert(Result['code'] == 0)
    assert(Result['out'].find('(1, 2)') > -1)
  
  def test_alias(self):
    Result = launch_ec('t1 arg1=1', '')
    
    assert(Result['code'] == 0)
    assert(Result['out'].find('(1, 2)') > -1)
  
if __name__ == '__main__':
  unittest.main()
