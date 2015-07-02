from core import execCommand
from classes import HandledException
from helpers import err

def init(argv):
  flag = argv.pop(0) if argv[0][0] == '-' else None
  
  if flag == '-h':
    return show_help()
  
  try:
    execCommand(argv, flag == '-p')
    
  except HandledException as e:
    err(e, 1)
    
def show_help(is_error=0):
  if is_error:
    err(get_help_text(), 1)
    
  else:
    print get_help_text()
    
def get_help_text():
  from helper_tasks import list_members
  
  text = '\n'.join(['Usage:',
    '  $ private module_path [flag] <command route> [args]',
    '\nFlags',
    ' -h    show help.',
    ' -p    execute a command with partial args.',
    '\nMembers\n',
  ]
  ) + '  ' + '\n  '.join([('%s  %s' % (name, desc))[:60] for name, desc in list_members('')])
  
  return text