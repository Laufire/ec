from ..modules.classes import CustomType

# Check: Escaping the separators.

class multi(CustomType):
  """Get a list of inputs.
  """
  def __init__(self, separator=', '):
    CustomType.__init__(self)
    
    self.separator = separator
    
  def __call__(self, val):
    return val.split(self.separator)
    
  def __str__(self):
    return 'a list of strings separated by \'%s\'' % self.separator

class some_of(CustomType):
  """Get mutilple items from a list of choices.
  """
  def __init__(self, choices, separator=', '):
    CustomType.__init__(self)
    
    self.choices = choices
    self.separator = separator
    
  def __call__(self, val):
    values = val.split(self.separator)
    
    if [value for value in values if value not in self.choices]:
      raise ValueError('Invalid value.')
     
    return values
    
  def __str__(self):
    return 'some of: %s' % self.separator.join(self.choices)
    
class one_of(CustomType):
  """Get a single item from a list of values.
  """
  def __init__(self, choices):
    CustomType.__init__(self)
    
    self.choices = choices
    
  def __call__(self, val):
    if not val in self.choices:
      raise ValueError('Invalid value.')
     
    return val
    
  def __str__(self):
    return '%s' % '/'.join(self.choices)
    
class menu(CustomType):
  """A numbered menu.
  """
  def __init__(self, choices):
    CustomType.__init__(self)
    
    self.choices = choices
    
  def __call__(self, val):
    try:
      val = int(val)
      
      if not 0 < val < len(self.choices):
        raise Exception('')
      
      return self.choices[val - 1]
      
    except:
      raise ValueError('Invalid value.')
    
  def __str__(self):
    ret = 'Select:\n'
    n = 0
    choices = self.choices
    
    for n in range(0, len(choices) - 1):
      ret += '\t%s: %s\n' % (n + 1, self.choices[n])
    
    return ret
