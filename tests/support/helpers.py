import shlex
from subprocess import Popen, STDOUT, PIPE

def shell_exec(command, path='.', input=''): # from gitapi.py
  print command
  proc = Popen(shlex.split(command), stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=path)
  
  out, err = [x.decode("utf-8") for x in proc.communicate(input)]
  
  return {'out': out, 'err': err, 'code': proc.returncode}
  