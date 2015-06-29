import shlex

from core import exec_command
from classes import HandledException

def init():
  while True:
    try:
      line = raw_input('>')
      
      exec_command(shlex.split(line), True)
      
    except HandledException as e:
      print e
      
    except EOFError: # ^z (null character) was passed
      exit()
  