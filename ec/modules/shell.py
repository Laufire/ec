"""
A module to handle the shell mode.
"""
import shlex

from core import execCommand, BaseGroup
from classes import HandledException, Group
from helpers import err

def init(**options):
  if options.get('helper_tasks'):
    import helper_tasks
    
    BaseGroup.Config['Members']['$'] = Group(helper_tasks, {'name': '$', 'desc': 'Shell mode Tasks.'})
    
  while True:
    try:
      line = raw_input('>')
      
      if line:
        result = execCommand(shlex.split(line), True)
        print '' if result is None else '%s\n' % str(result)
        
    except HandledException as e:
      err('%s\n' % e)
      
    except EOFError: # ^z (null character) was passed
      exit()
  