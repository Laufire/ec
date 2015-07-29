"""
utils
=====

A set of utility functions for the scripts.
"""
from modules.exposed import get, static
from modules.classes import CustomType

__all__ = ['get', 'static', 'custom']

class custom(CustomType):
  """Helps with creating dynamic CustomTypes on the fly.
  
  Args:
    validator (callable): Validates the input.
    converter (callable): Converts the input. Defaults to None.
    **Config  (kwargs): The configuration of the CustomType.
  """
  def __init__(self, validator, converter=None, **Config):
    CustomType.__init__(self, **Config)
    
    self.validator = validator
    self.converter = converter
    
  def __call__(self, val):
    if self.converter:
      val = self.converter(val)
      
    if not self.validator(val):
      raise ValueError()
      
    return val
    