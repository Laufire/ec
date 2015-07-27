"""
Test ec.utils.
"""
import unittest

from ec.utils import get, static, custom

from support.helpers import RawInputHook as RIH, expect_exception

# Tests
class TestUtils(unittest.TestCase):

  def setUp(self):
    pass

  def tearDown(self):
    pass
    
  def test_get(self):
    Inputs = 'a', 1
    RIH.values(*Inputs)
    
    # test the call
    assert(get('str') == Inputs[0])
    
    assert(get('int', type=int) == Inputs[1])
    
  def test_static(self):
    @static
    class cls:
      def method(val):
        return val
        
    assert(cls.method(1) == 1)
    
  def test_custom(self):
    _type = custom(lambda v: v%2==1, 'an odd number', int)
    
    assert(_type(1) == 1)
    assert(expect_exception(lambda: _type(2), ValueError))
    assert(expect_exception(lambda: _type('a'), ValueError))
  
if __name__ == '__main__':
  unittest.main()
