"""
Tests the inscript calls
"""

import unittest

from ec.ec import call

from targets.simple import task1, group1
from support.helpers import RawInputHook as RIH

# Tests
class TestInscriptCalls(unittest.TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass
    
  def test_task_call(self):
    """Test whether the tasks are callable as functions.
    """
    assert(task1(1) == (1, 2))
    
  def test_group_task_call(self):
    """Test whether the group tasks are callable as (static) functions.
    """
    assert(group1.task1(1) == 1)
    
  def test_ec_call(self):
    """Test ec.call with partial arguments
    """
    RIH.values(2, 3)
    assert(call(task1, arg1=1) == (1, 2))
  
if __name__ == '__main__':
  unittest.main()
