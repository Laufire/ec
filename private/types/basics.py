from ..modules.classes import CustomType

class yn(CustomType):
  """
  The classic y / n input that returns a truthy / falsy value.
  """
  def __init__(self, desc=None):
    CustomType.__init__(self, desc if desc is not None else 'y/n')
  
  def __call__(self, val):
    if val in 'yY':
      return 1
    
    elif val in 'nN':
      return 0
      
    else:
      raise ValueError('Invalid value.')
      