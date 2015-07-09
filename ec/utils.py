"""
utils
=====

A set of utility functions for the scripts.
"""
from modules.helpers import err

def get(desc, type=None, autoDesc=True, **Kwargs):
  """Helps to interactively get user input.
  
  Args:
    desc (str): The description for input.
    type (type / CustomType): The type of the input (defaults to None).
    autoDesc (bool): When set to false, it suppresses the generation of the prompt string based on the given arguments (defaults to True).
    default: The default value for the input.
    
  Notes:
    * The arg **default** is made to be a part pf Kwargs, rather than an explicit argument, in order to allow the declaration of 'None' as the default value.
  """
  has_default = 'default' in Kwargs
  default = Kwargs.get('default')
  label = '%s: ' % ('%s%s' % (desc, ', %s' % type if isinstance(type, CustomType) else '') if autoDesc else desc)
  
  while True:
    try:
      line = raw_input(label)
      
      if has_default and not line:
        return default
      
      got = line
      
    except EOFError: # consider ^z as None
    
      got = None
      
    try:
      return type(got) if type else got
      
    except ValueError:
      err('<invalid value>')
      
    except TypeError:
      err('<invalid value>')
  
# Cross dependencies
from modules.classes import CustomType
