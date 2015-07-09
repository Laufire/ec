"""
num
====
Types for handling numbers.
"""
from ..modules.classes import CustomType

class between(CustomType):
  """Get a number within two numbers.
  """
  def __init__(self, min, max, num_type=int):
    CustomType.__init__(self)
    
    self.min = min
    self.max = max
    self.num_type = num_type
    
  def __call__(self, val):
    value = self.num_type(val)
    
    if value < self.min or value > self.max:
      raise ValueError()
    
    return value
    
  def __str__(self):
    return 'a number between %s and %s' % (self.min, self.max)
