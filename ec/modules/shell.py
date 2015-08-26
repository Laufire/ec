r"""
A module to handle the shell mode.
"""
import shlex

from state import Settings
from core import execCommand, BaseGroup
from classes import HandledException, Group
from helpers import err, split, exit

def init():
  if Settings.get('helper_tasks', True):
    import helper_tasks
    helper_tasks.main()
    
  while True:
    try:
      line = raw_input('>')
      
      if line:
        result = execCommand(split(line), True)
        print '' if result is None else '%s\n' % str(result)
        
    except HandledException as e:
      err('%s\n' % e)
      
    except EOFError: # ^z (null character) was passed
      exit()
  