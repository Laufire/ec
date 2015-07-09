"""
basics
======
Basic types, like bool and the likes.
"""
from ..modules.classes import CustomType

# Check: is it possible to use yn as a singleton as well as a constructor. ie: yn refers to an instance with default values,
# where as yn(...) could be used to get a customized yn.

class yn(CustomType):
  """The classic y/n input that returns a truthy/falsy value.
  """
  def __init__(self, desc=None, default=None):
    label = desc if desc is not None else ('y/n%s' % ((' (%s)' % 'y' if default else 'n') if default is not None else ''))
    
    CustomType.__init__(self, label)
    self.default = default
  
  def __call__(self, val):
    if val in 'yY':
      return True
    
    elif val in 'nN':
      return False
      
    elif self.default is not None:
      return self.default
      
    else:
      raise ValueError()
      