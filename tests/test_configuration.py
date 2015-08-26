r"""
Tests ec.interface.

Note:
  This test might fail when tested over the devlopment dir (or its symlinks), hence it should be run on the installed package.  
"""
import unittest

from ec import interface

from targets import simple

interface.setBase(simple)

class TestConfiguration(unittest.TestCase):
  def setUp(self):
    pass
    
  def tearDown(self):
    pass

  def test_verify_configuration(self):
    Members = simple.__ec_member__.Members
    
    assert(set(['task1', 't1', 'group1', 'ex', 'hex']) == set(Members.keys()))
    assert(set(['task1']) == set(Members['group1'].Members.keys()))

if __name__ == '__main__':
  unittest.main()
