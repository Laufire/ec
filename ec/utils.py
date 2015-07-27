"""
utils
=====

A set of utility functions for the scripts.
"""
from modules.exposed import get, static
from modules.classes import CustomType

__all__ = ['get', 'static', 'custom']
  
def custom(validator, desc=None, converter=None):
  """Helps with creating dynamic CustomTypes on the fly.
  
  Args:
    validator (callable): that acts as the converter / validator.
    desc (str): the desc to be dispalyed on the helps. Defaults to None.
    converter (callable):  A callable that converts the given value. Defaults to None.
  """
  class dynamic(CustomType):
    def __init__(self):
      CustomType.__init__(self, desc)
      
    def __call__(self, val):
      if converter:
        val = converter(val)
        
      if not validator(val):
        raise ValueError()
        
      return val
    
  return dynamic()