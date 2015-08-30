"""
path
====
Types for handling paths.
"""
from os import path

from ..modules.classes import CustomType

class PathBase(CustomType):
  """The base class for several path types.

  Args:
    func (callable): The function to process the value.
    ret : The expected return value from func. The values that ail the expectation are invalid.
    **Config (kwargs): Configuration for the custom type.
  """
  def __init__(self, func, ret=True, **Config):
    CustomType.__init__(self, **Config)

    self.func = func
    self.ret = ret

  def __call__(self, val):
    if self.func(val) == self.ret:
      return val

    raise ValueError()

exists = PathBase(path.exists, type_str='an existing path')
free = PathBase(path.exists, False, type_str='a free path')
isdir = PathBase(path.isdir, type_str='a dir')
isfile = PathBase(path.isfile, type_str='a file')
isabs = PathBase(path.isabs, type_str='an absolute path')
isrelative = PathBase(path.isabs, False, type_str='a relative path')
ischild = PathBase(path.isabs, False, type_str='a relative path')

def exists_in(root): # ToDo: Replace this function with a CustomType based class
  return PathBase(lambda val: path.exists(path.join(root, val)), type_str='a path under %s' % root)
