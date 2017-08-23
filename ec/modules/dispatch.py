r"""
A module to handle the dispatch mode.
"""

from core import execCommand
from classes import HandledException
from helpers import err, getMemberHelp, getRouteHelp

def init(argv):
  flag = argv.pop(0) if argv[0][0] == '-' else None

  if flag == '-h':
    help_text = get_help_text(argv)

    if help_text is None:
      err('Can\'t help :(')

    else:
      print help_text

  else:
    try:
      ret = execCommand(argv, flag == '-p')
      # Check: Should the dispatch mode log the return value? It isn't logging it now to keep the console from excess output.

      if ret is not None:
        print ret

    except HandledException as e:
      Member = e.Info.get('Member')

      if Member:
        alias = Member.Config.get('alias')
        name = Member.Config['name']

        if name == '__main__':
          name = 'Members'

        label = '%s%s' % (name, ', %s' % alias if alias else '')
        e = '%s\n\n%s\n%s\n%s' % (str(e), label, '-' * len(label), getMemberHelp(Member))

      err(e, 1)

def get_help_text(argv):
  if argv:

    return getRouteHelp(argv[0].split('/'))

  else:

    return '\n'.join(['Usage:',
      '  $ ec module_path [flag] <command route> [args]',
      '\nFlags',
      ' -h    show help.',
      ' -p    execute a command with partial args.',
      '\nMembers\n-------\n',
      getRouteHelp([]),
    ]
    )
