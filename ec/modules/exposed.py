"""
exposed
=======

A module for members that are used by ec, as well as exposed to the scripts.

"""
def get(desc='', type=None, **KwArgs):
  """Helps to interactively get user input.
  
  Args:
    desc (str): The description for input.
    type (type / CustomType): The type of the input (defaults to None).
    
  Notes:
    * When 'desc' is not provided, the Kwarg 'name' and 'type_str' are expected; which will be used to generate a description.
    * KwArgs acts as a data container for unexpected attibutes that are used by underlying helpers.
  """
  if not desc:
    desc = getAutoDesc(KwArgs)
    
  while True:
    try:
      got = raw_input('%s: ' % desc)
      
    except EOFError:
      got = None
      
    if not got and 'default' in KwArgs:
      return KwArgs['default']
    
    try:
      return type(got) if type else got
      
    except ValueError:
      err('<invalid value>')
      
    except TypeError:
      err('<invalid value>')
  
def static(cls):
  """Converts the given class into a static one, by changing all the methods of it into static methods.
  
  Args:
    cls (class): The class to be converted.
  """
  for attr in dir(cls):
      im_func = getattr(getattr(cls, attr), 'im_func', None)
      if im_func:
        setattr(cls, attr, staticmethod(im_func))
  
  return cls
  
# Cross dependencies
from helpers import err, getAutoDesc
from classes import CustomType
