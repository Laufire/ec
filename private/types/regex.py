import re

from ..modules.classes import CustomType

class pattern(CustomType):
  """
  Used to restrict the input to specific patterns.
  """
  def __init__(self, pattern, flags=0, desc=None):
    self.exp = re.compile(pattern, flags)
    if desc is not None:
      self.desc = desc
      
  def __call__(self, val):
    if not self.exp.match(val):
      raise ValueError('Invalid value.')
      
    return val
    
  def __str__(self):
    return getattr(self, 'desc', 'a string matching the pattern \'%s\'' % self.exp.pattern)
    
email = pattern('^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$', desc='Email')
username = pattern('^[a-z0-9_-]{3,16}$', desc='Username')
password = pattern('^[A-z0-9_-]{6,18}$', desc='Password')
slug = pattern('^[a-z0-9-]+$', desc='Slug')
