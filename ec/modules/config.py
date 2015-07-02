import sys

from classes import Task, Group, HandledException
from helpers import get_calling_module, err

__all__ = ['task', 'arg', 'group', 'module']

# Decorators
def task(Func=None, **Config):
  """A decorator to make tasks out of functions."""
  return _task(Func, Config) if Func else lambda Func: _task(Func, Config)

def arg(name, **Config):
  """A decorator to configure an argument of a task.
  
    * It always follows a @task or an @arg.
  """
  return lambda Func: _arg(name, Func, Config)
  
def group(Underlying=None, **Config):
  """A decorator to make groups out of classes."""
  return _group(Underlying, Config) if Underlying else lambda Underlying: _group(Underlying, Config)

# Methods
def module(**Config):
  """Helps with adding configs to Modules.
  """
  Underlying = get_calling_module()
  Group(Underlying).Config.update(**Config)

# Workers - does the actual work within the decorators
def _task(Func, Config):
  _Task = _wrapObject(Func, Task)
  _Task.Config.update(**Config)
  
  try:
    _Task.__prepare__()
    
  except HandledException as e:
    err(e, 1)
  
  return _Task.Underlying

def _arg(name, Func, Config):
  _Task = _wrapObject(Func, Task)
  _Task.Args.insert(0, (name, Config))
  
  return _Task
  
def _group(Underlying, Config):
  _Group = Group(Underlying)
  _Group.Config.update(**Config)
  
  return _Group.Underlying
  
# Helpers
def _wrapObject(Obj, Wrapper):
  return Obj if isinstance(Obj, Wrapper) else Wrapper(Obj)
  