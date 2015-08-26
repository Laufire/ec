r"""
Tests the shell mode.
"""

import unittest

from support.helpers import shell_exec, checkResult


def launch_ec(*lines):
  """Passes commands through the shell.
  """
  return shell_exec('python tests/targets/simple.py', input='%s\n\0' % '\r\n'.join(lines))

class TestShell(unittest.TestCase):
  def setUp(self):
    self.checkResult = lambda *args: checkResult(self, *args)

  def tearDown(self):
    pass
    
  def test_task(self):
    Result = launch_ec('task1', '1', '2', '3')
    
    self.checkResult(Result,
      Result['code'] == 0,
      Result['out'].find('(1, 2)') > -1,
    )
    
  def test_multiple_args(self):
    Result = launch_ec('task1 arg1=1 arg2=1')
    
    self.checkResult(Result,
      Result['code'] == 0,
      Result['out'].find('(1, 1)') > -1,
    )
    
  def test_help(self):
    Result = launch_ec('h', '')
    out = Result['out']
    
    self.checkResult(Result,
      Result['code'] == 0,
      out.find('task1') > -1,
      out.find('group1') > -1,
      out.find('task1') > -1,
    )
  
  def test_absent_task(self):
    Result = launch_ec('task2')
    
    self.checkResult(Result,
      Result['code'] == 0,
      Result['err'].strip()[:2] == 'No',
    )
    
  def test_nested_task(self):
    Result = launch_ec('group1/task1 arg1=100000')
    
    self.checkResult(Result,
      Result['code'] == 0,
      Result['out'].find('100000') > -1,
    )

  def test_default_arg(self):
    Result = launch_ec('task1 arg1=1', '')
    
    self.checkResult(Result,
      Result['code'] == 0,
      Result['out'].find('(1, 2)') > -1,
    )
  
  def test_alias(self):
    Result = launch_ec('t1 arg1=1', '')
    
    self.checkResult(Result,
      Result['code'] == 0,
      Result['out'].find('(1, 2)') > -1,
    )
  
if __name__ == '__main__':
  unittest.main()
