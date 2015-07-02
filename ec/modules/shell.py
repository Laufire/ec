import shlex

from core import execCommand, BaseGroup
from classes import HandledException, Group

def init(**options):
  if options.get('helper_tasks'):
    import helper_tasks
    
    BaseGroup.Config['Members']['$'] = Group(helper_tasks)
    
  while True:
    try:
      line = raw_input('>')
      
      if line:
        execCommand(shlex.split(line), True)
      
    except HandledException as e:
      print e
      
    except EOFError: # ^z (null character) was passed
      exit()
  