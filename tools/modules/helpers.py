import os
import sys
from os import path
import shlex
from subprocess import Popen, PIPE
from shutil import rmtree as _rmtree
import win32file

def shell_exec(command, **kwargs): # from gitapi.py
  """Excecutes the given command silently.
  """
  proc = Popen(shlex.split(command), stdout=PIPE, stderr=PIPE, **kwargs)

  out, err = [x.decode("utf-8") for x in  proc.communicate()]

  return {'out': out, 'err': err, 'code': proc.returncode}

def err(message, exit_code=None):
  sys.stderr.write('%s\n' % message)

  if exit_code is not None:
    exit(exit_code)

def run(command, **kwargs):
  """Excecutes the given command while transfering control, till the execution is complete.
  """
  print command
  p = Popen(shlex.split(command), **kwargs)
  p.wait()

  return p.returncode

def rmtree(dir):
  if path.isdir(dir):
    _rmtree(dir)

def get_relative(file_path, relation):
  return path.abspath(path.abspath(path.split(file_path)[0]) +  relation)

def unlink(target_path):
  if path.isfile(target_path):
    os.unlink(target_path)

def rmdir(target_path):
  if path.isdir(target_path):
    os.rmdir(target_path)

def make_link(source_path, target_path): # links two paths. Files are hard linked, where as dirs are linked as junctions.
  if path.isfile(source_path):
    unlink(target_path)
    win32file.CreateHardLink(target_path, path.abspath(source_path))

  elif path.isdir(source_path):
    rmdir(target_path)

    win32file.CreateSymbolicLink(target_path, path.abspath(source_path), 1)

  else:
    return 1 # error
