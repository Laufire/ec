"""
basics
======
Basic types, like bool and the likes.
"""
from ..modules.classes import CustomType

class YN(CustomType):
  """The classic y/n input that returns a truthy/falsy value.
  """
  def __init__(self, **Config):
    if not 'type_str' in Config:
      Config['type_str'] = 'y/n'

    CustomType.__init__(self, **Config)

  def __ec_config__(self, ArgConfig):
    ArgConfig['type_str'] = '%s%s' % (self.str, (' (%s)' % ('y' if ArgConfig['default'] else 'n')) if 'default' in ArgConfig else '')

    return ArgConfig

  def __call__(self, val):
    if not val: # we've got an empty string
      raise ValueError()

    if val in 'yY':
      return True

    elif val in 'nN':
      return False

    raise ValueError()

yn = YN()
