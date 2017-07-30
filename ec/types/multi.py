r"""
multi
=====
Types for handling lists and list members.

ToDos
=====
* Error messages show the types as **custom type**, listing the options would be better.
"""

from ..modules.classes import CustomType

# Check: Escaping the separators.

class multi(CustomType):
  """Get a list of inputs, separated by the given separator.
  """
  def __init__(self, separator=', ', **Config):
    if not 'type_str' in Config:
      Config['type_str'] = 'a list of strings separated by \'%s\'' % separator

    CustomType.__init__(self, **Config)

    self.separator = separator

  def __call__(self, val):
    return val.split(self.separator)

class some_of(CustomType):
  """Get mutilple items from a list of choices.
  """
  def __init__(self, choices, separator=', ', **Config):
    if not 'type_str' in Config:
      Config['type_str'] = 'some of: %s' % separator.join(choices)

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
    if not 'type_str' in Config:
      Config['type_str'] = 'one of %s' % Config.get('sep', ' / ').join(choices)

    CustomType.__init__(self, **Config)

    self.choices = choices

  def __call__(self, val):
    if not val in self.choices:
      raise ValueError()

    return val

class menu(CustomType):
  """A numbered menu.
  """
  def __init__(self, choices, **Config):
    if not 'type_str' in Config:
      Config['type_str'] = self._get_str(choices)

    CustomType.__init__(self, **Config)

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
