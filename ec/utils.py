"""
Utils
=====
A set of utility functions for the scripts.
"""
from modules.helpers import err

def get(desc=None, type=None, **Kwargs):
  """Helps to interactively get user input."""
  while True:
    try:
      line = raw_input('%s: ' % desc)
      
      if not line:
        if 'default' in Kwargs:
          return Kwargs['default']
      
      got = line
      
    except EOFError: # consider ^z as None
    
      got = None
      
    try:
      return type(got) if type else got
      
    except ValueError:
      err('<invalid value>')
      
    except TypeError:
      err('<invalid value>')
  