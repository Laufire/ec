r"""
Tests the dispatch mode.

Notes:

  * This test is used as the base by several other tests.
"""

import unittest

from support.helpers import shell_exec, checkResult

# Tests
class TestDispatch(unittest.TestCase):
  def setUp(self):
    self.checkResult = lambda *args: checkResult(self, *args)

  def tearDown(self):
    pass

  def launch_ec(self, argStr='', input='', flag=''):
    r"""Dispatches command to the target script.
    """
    command = 'python tests/targets/simple.py'

    if flag:
      command += ' %s' % flag

    if argStr:

      command += ' %s' % argStr

    return shell_exec(command, input=input)

  def test_dispatch(self):
    Result = self.launch_ec('task1 arg1=1')

    self.checkResult(Result,
      Result['code'] == 0,
      Result['out'].strip() == '1 2',
    )

  def test_multiple_args(self):
    Result = self.launch_ec('task1 arg1=1 arg2=1')

    self.checkResult(Result,
      Result['code'] == 0,
      Result['out'].strip() == '1 1',
    )

  def test_positional_args(self):
    Result = self.launch_ec('task1 1')

    self.checkResult(Result,
      Result['code'] == 0,
      Result['out'].strip() == '1 2',
    )

  def test_mixed_args(self):
    Result = self.launch_ec('task1 1 arg2=1')

    self.checkResult(Result,
      Result['code'] == 0,
      Result['out'].strip() == '1 1',
    )

  def test_flag_help(self):
    Result = self.launch_ec(flag='-h')

    self.checkResult(Result,
      Result['code'] == 0,
      Result['out'].strip()[:5] == 'Usage',
    )

  def test_flag_help_task(self):
    Result = self.launch_ec(flag='-h', argStr='task1')

    self.checkResult(Result,
      Result['code'] == 0,
      Result['out'].find('Args:') > -1,
    )

  def test_flag_help_group(self):
    Result = self.launch_ec(flag='-h', argStr='group1')

    self.checkResult(Result,
      Result['code'] == 0,
      Result['out'].find('task1') > -1,
    )

  def test_flag_help_subgroup(self):
    Result = self.launch_ec(flag='-h', argStr='group1/task1')

    self.checkResult(Result,
      Result['code'] == 0,
      Result['out'].find('Args:') > -1,
    )

  def test_flag_partial(self):
    Result = self.launch_ec('task1 arg1=1', '1', '-p')

    self.checkResult(Result,
      Result['code'] == 0,
      Result['out'][-5:-1].strip() == '1 1'
    )

  def test_absent_task(self):
    Result = self.launch_ec('task2')

    self.checkResult(Result,
      Result['code'] == 1,
      Result['err'].strip()[:2] == 'No',
      Result['err'].find('------') > -1, # check whether a help string is presented
    )

  def test_nested_task(self):
    Result = self.launch_ec('group1/task1 arg1=1')

    self.checkResult(Result,
      Result['code'] == 0,
      Result['out'].strip() == '1',
    )

  def test_default_arg(self):
    Result = self.launch_ec('task1 arg1=1')

    self.checkResult(Result,
      Result['code'] == 0,
      Result['out'].strip() == '1 2',
    )

  def test_alias(self):
    Result = self.launch_ec('t1 arg1=1')

    self.checkResult(Result,
      Result['code'] == 0,
      Result['out'].strip() == '1 2',
    )

  def test_handled_exception(self):
    Result = self.launch_ec('hex')
    err = Result['err']

    self.checkResult(Result,
      Result['code'] == 1,
      err.find('Invalid') > -1,
      err.find('arg1') > -1,
      err.find('int') > -1,
      err.find('got') > -1,
    )

  def test_exception(self):
    Result = self.launch_ec('ex')

    self.checkResult(Result,
      Result['code'] == 1,
      Result['err'].strip() == 'integer division or modulo by zero',
    )

  def test_exit_hook(self):
    Result = shell_exec('python tests/targets/allied.py t1 1')

    self.checkResult(Result,
      Result['code'] == 0,
      Result['out'].find(str(range(1, 10))) > -1,
    )

if __name__ == '__main__':
  unittest.main()
