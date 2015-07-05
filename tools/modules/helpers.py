import os
from os import path
import shlex
from subprocess import Popen, STDOUT, PIPE
from shutil import rmtree as _rmtree

def shell_exec(command, path='.'): # from gitapi.py	
	proc = Popen(shlex.split(command), stdout=PIPE, stderr=PIPE, cwd=path)

	out, err = [x.decode("utf-8") for x in  proc.communicate()]

	return {'out': out, 'err': err, 'code': proc.returncode}
  
def rmtree(dir):
  path.isdir(dir) and _rmtree(dir)
  
def get_relative(file_path, relation):
  return path.abspath(path.split(file_path)[0] +  relation)