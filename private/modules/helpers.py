import sys

def err(message, exit_code=None):
  sys.stderr.write('%s\n' % message)
  
  if exit_code is not None:
    exit(exit_code)