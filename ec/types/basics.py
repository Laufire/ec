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
  def __init__(self, **Config):
    if not 'type_str' in Config:
      Config['type_str'] = 'y/n%s' % (' (%s)' % ('y' if Config['default'] is True else 'n') if 'default' in Config else '')
    
    CustomType.__init__(self, **Config)
    
  def __ec_config__(self, ArgConfig):
    if not 'desc' in ArgConfig:
      ArgConfig['desc'] = ArgConfig['name']
    
  def __call__(self, val):
    if not val: # we've got an empty string
      raise ValueError()
      
    if val in 'yY':
      return True
    
    elif val in 'nN':
      return False
      
    raise ValueError()
    