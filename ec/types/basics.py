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
  def __init__(self, desc=None, **kwargs):
    """
    Note:
      kwargs is used instead of an explcit var named default, as **None** too could be the default value.
    """
    has_default = 'default' in kwargs
    default = kwargs['default'] if has_default else None
    
    label = desc if desc is not None else ('y/n%s' % (' (%s)' % ('y' if default is True else ('n' if default is False else default)) if has_default else ''))
    
    CustomType.__init__(self, label)
    
    if has_default:
      self.default = default
  
  def __call__(self, val):
    if not val:
      return self.__default__()
      
    if val in 'yY':
      return True
    
    elif val in 'nN':
      return False
      
    return self.__default__()
    
  def __default__(self):
    if hasattr(self, 'default'):
      return self.default
      
    else:
      raise ValueError()
      