"""
A module to handle the dispatch mode.
"""

from core import execCommand, BaseGroup
from classes import HandledException
from helpers import err, listMemberHelps

def init(argv):
  flag = argv.pop(0) if argv[0][0] == '-' else None
  
  if flag == '-h':
    print get_help_text()
    return
    
  try:
    execCommand(argv, flag == '-p')
    # Check: Should the dispatch mode log the return value? It isn't logging it now to keep the console from excess output.
    
  except HandledException as e:
    err(e, 1)
    
def get_help_text():
  text = '\n'.join(['Usage:',
    '  $ ec module_path [flag] <command route> [args]',
    '\nFlags',
    ' -h    show help.',
    ' -p    execute a command with partial args.',
    '\nMembers\n',
  ]
  ) + '  ' + '\n  '.join([('%s  %s' % (name, desc))[:60] for name, desc in listMemberHelps(BaseGroup)])
  
  return text
  