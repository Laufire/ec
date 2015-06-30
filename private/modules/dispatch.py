from core import execCommand
from classes import HandledException
from helpers import err

def init(argv):
  try:
    execCommand(argv, False)
    
  except HandledException as e:
    err(e, 1)
    