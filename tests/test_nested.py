"""
Tests nested scripts.

Note:
  The test cases for this test are provided by test_dispatch.
"""

import unittest

from support.helpers import shell_exec

# Modifications to test_dispatch
import test_dispatch

test_dispatch.script_name = 'support/nester.py'
test_dispatch.command_prefix = 'target_script/'

TestNested = test_dispatch.TestDispatch

if __name__ == '__main__':
  unittest.main()
