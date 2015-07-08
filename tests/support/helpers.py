import shlex
from subprocess import Popen, STDOUT, PIPE

def shell_exec(command, path='.'): # from gitapi.py	
	proc = Popen(shlex.split(command), stdout=PIPE, stderr=PIPE, cwd=path)

	out, err = [x.decode("utf-8") for x in  proc.communicate()]

	return {'out': out, 'err': err, 'code': proc.returncode}
  