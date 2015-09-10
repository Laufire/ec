r"""
Tests nested scripts.

Note:
  The test cases for this test are provided by test_dispatch.
"""

import unittest

from support.helpers import shell_exec

from test_dispatch import TestDispatch

class TestNested(TestDispatch):
  def launch_ec(self, argStr='', input='', flag=''):
    """Dispatches command to a nested script.
    """

    command = 'python tests/targets/nester.py'

    if flag:
      command += ' %s' % flag

    if argStr:

      command += ' simple/%s' % argStr

    return shell_exec(command, input=input)

if __name__ == '__main__':
  unittest.main()
