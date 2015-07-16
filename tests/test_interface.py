"""
Test ec.interface.
"""
import unittest

from ec import interface

from support import target_script

interface.setBase(target_script)

class TestInterface(unittest.TestCase):

  def setUp(self):
    pass
    
  def tearDown(self):
    pass

  def test_call(self):
    assert(interface.call('task1 arg1=1') == (1, 2))
    
  def test_call_with_input(self):
    # Hook into existing raw_input
    import __builtin__
    origCall = __builtin__.raw_input
    __builtin__.raw_input = lambda dummy: 2
    
    # test the call
    assert(interface.call('task1 arg1=1', True) == (1, 2))
    
    # remove the hook
    __builtin__.raw_input = origCall
    
  def test_resolve(self):
    assert(interface.resolve('task1').Config['name'] == 'task1')
    
  def test_args(self):
    Args = interface.resolve('task1').Args
    
    assert(len(Args.keys()) == 3)
    
    # Check Arg Order
    Order = ['arg1', 'arg2', 'arg3']
    for k in Args.keys():
      assert(k == Order.pop(0))
      
    arg1 = Args['arg1']
    
    assert(arg1['desc'] == 'Value for arg1')
    assert(arg1['type'] == int)
    
  def test_group(self):
    Group1 = interface.resolve('group1')
    Config = Group1.Config
    Members = Group1.Members
    Members = Group1.Members
    
    assert(len(Members.keys()) == 1)
    assert(Members['task1'] is not None)
    assert(Config['desc'] == 'Description for group1')
    
if __name__ == '__main__':
  unittest.main()
