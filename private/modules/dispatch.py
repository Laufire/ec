from core import exec_command
from classes import HandledException
from helpers import err

def init(argv):
  try:
    exec_command(argv, False)
    
  except HandledException as e:
    err(e, 1)
    