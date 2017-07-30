r"""
A module to handle the shell mode.
"""
from sys import stdin
from state import Settings
from core import execCommand
from classes import HandledException
from helpers import err, split, exit

def init():
  if Settings.get('helper_tasks', True):
    import helper_tasks
    helper_tasks.main()


  def worker(line):
    try:
      result = execCommand(split(line), True)
      print '' if result is None else '%s\n' % str(result)

    except HandledException as e:
      err('%s\n' % e)

  if stdin.isatty(): # Enter interactive shell

    prompt = Settings.get('prompt', '>')

    while True:
      try:
        line = raw_input(prompt)

        if line:
          worker(line)

      except EOFError: # ^z (null character) was passed.
        exit()

  else:

    for line in stdin.readlines():
      worker(line.strip('\r\n ')) # #Pending: As of now, stdin should provide whole commands. Commands and argoments couldn't be separated into multiple lines (like with the interactive mode). Fix this,
