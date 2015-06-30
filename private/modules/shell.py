import shlex

from core import execCommand
from classes import HandledException

def init():
  while True:
    try:
      line = raw_input('>')
      
      execCommand(shlex.split(line), True)
      
    except HandledException as e:
      print e
      
    except EOFError: # ^z (null character) was passed
      exit()
  