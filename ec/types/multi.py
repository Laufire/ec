"""
multi
=====
Types for handling lists and list members.
"""
from ..modules.classes import CustomType

# Check: Escaping the separators.

class multi(CustomType):
  """Get a list of inputs.
  """
  def __init__(self, separator=', '):
    self.str = 'a list of strings separated by \'%s\'' % separator
    CustomType.__init__(self)

    self.separator = separator

  def __call__(self, val):
    return val.split(self.separator)

class some_of(CustomType):
  """Get mutilple items from a list of choices.
  """
  def __init__(self, choices, separator=', ', **Config):
    self.str = 'some of: %s' % separator.join(choices)
    CustomType.__init__(self, **Config)

    self.choices = choices
    self.separator = separator

  def __call__(self, val):
    values = val.split(self.separator)

    if [value for value in values if value not in self.choices]:
      raise ValueError()

    return values

class one_of(CustomType):
  """Get a single item from a list of values.
  """
  def __init__(self, choices, **Config):
    self.str = 'one of %s' % '/'.join(choices)
    CustomType.__init__(self, **Config)

    self.choices = choices

  def __call__(self, val):
    if not val in self.choices:
      raise ValueError()

    return val


class menu(CustomType):
  """A numbered menu.
  """
  def __init__(self, choices):
    self.str = self._get_str(choices)
    CustomType.__init__(self)

    self.choices = choices

  def __call__(self, val):
    try:
      val = int(val)

      if not 0 < val <= len(self.choices):
        raise Exception('')

      return self.choices[val - 1]

    except:
      raise ValueError()

  def _get_str(self, choices):
    ret = 'Menu:\n'
    n = 0

    for n in range(0, len(choices)):
      ret += '\t%s: %s\n' % (n + 1, choices[n])

    return ret
