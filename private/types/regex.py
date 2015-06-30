import re

class pattern:
  def __init__(self, pattern, flags=0):
    self.exp = re.compile(pattern, flags)
    
  def __call__(self, val):
    if not self.exp.match(val):
      raise ValueError('Invalid value.')
      
    return val
    
  def __str__(self):
    return 'a string matching the pattern \'%s\'' % self.exp.pattern
    