r"""
Tests nested scripts.

Note:
  The test cases for this test are provided by test_dispatch.
"""

import unittest

from support.helpers import shell_exec

from test_dispatch import TestDispatch

class TestModuleLaunch(TestDispatch): #pylint: disable=R0801
  def launch_ec(self, argStr='', input='', flag=''):
    r"""Dispatches command to ec (loaded as a module).
    """  
    command = 'python -m ec tests/targets/simple.py'
    
    if flag:
      command += ' %s' % flag
      
    if argStr:
      
      command += ' %s' % argStr
      
    return shell_exec(command, input=input)

if __name__ == '__main__':
  unittest.main()
