r"""
num
====
Types for handling numbers.
"""
from ..modules.classes import CustomType

class between(CustomType):
  """Get a number within two numbers.
  """
  def __init__(self, min, max, num_type=int, **Config):

    if not 'type_str' in Config:
      Config['type_str'] = 'a number between %s and %s' % (min, max)

    CustomType.__init__(self, **Config)

    self._min = min
    self._max = max
    self._num_type = num_type

  def __call__(self, val):
    value = self._num_type(val)

    if value < self._min or value > self._max:
      raise ValueError()

    return value
