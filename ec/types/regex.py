
"""
regex
=====
Types based on regular expressions.
"""

import re

from ..modules.classes import CustomType

class pattern(CustomType):
  """Get inputs that fit a specific pattern.
  """
  def __init__(self, pattern, flags=0, desc=None):
    CustomType.__init__(self, desc)
    self.exp = re.compile(pattern, flags)
    
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
number = pattern('^[0-9]+$', desc='Number') # a positive integer
