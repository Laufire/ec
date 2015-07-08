"""
A module to handle the dispatch mode.
"""

from core import execCommand
from classes import HandledException
from helpers import err

def init(argv):
  flag = argv.pop(0) if argv[0][0] == '-' else None
  
  if flag == '-h':
    print get_help_text()
    return
    
  try:
    execCommand(argv, flag == '-p')
    
  except HandledException as e:
    err(e, 1)
    
def get_help_text():
  from helper_tasks import listMemberHelps
  
  text = '\n'.join(['Usage:',
    '  $ ec module_path [flag] <command route> [args]',
    '\nFlags',
    ' -h    show help.',
    ' -p    execute a command with partial args.',
    '\nMembers\n',
  ]
  ) + '  ' + '\n  '.join([('%s  %s' % (name, desc))[:60] for name, desc in listMemberHelps('')])
  
  return text
  