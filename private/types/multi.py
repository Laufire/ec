from ..modules.classes import CustomType

class multi(CustomType):
  """
  Used to get a list of inputs.
  """
  def __init__(self, separator=', '):
    self.separator = separator
    
  def __call__(self, val):
    return val.split(self.separator)
    
  def __str__(self):
    return getattr(self, 'desc', 'a list of strings separated by \'%s\'' % self.separator)

class some_of(CustomType):
  def __init__(self, choices, separator=', '):
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
  def __init__(self, choices):
    self.choices = choices
    
  def __call__(self, val):
    if not val in self.choices:
      raise ValueError('Invalid value.')
     
    return val
    
  def __str__(self):
    return '%s' % '/'.join(self.choices)
