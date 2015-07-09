
"""
path
====
Types for handling paths.
"""

from os import path

from ..modules.classes import CustomType

class PathBase(CustomType):
  """The base class for several path types."""
  
  def __init__(self, func, ret=True, desc=None):
    CustomType.__init__(self, desc)
    
    self.func = func
    self.ret = ret
    
  def __call__(self, val):
    if self.func(val) == self.ret:
      return val
      
    raise ValueError('Invalid value.')
    
  def __str__(self):
    return getattr(self, 'desc', '')

exists = PathBase(path.exists, desc='an existing path')
free = PathBase(path.exists, False, 'a free path')
isdir = PathBase(path.isdir, desc='a dir')
isfile = PathBase(path.isfile, desc='a file')
isabs = PathBase(path.isabs, desc='an absolute path')
isrelative = PathBase(path.isabs, False, 'a relative path')
