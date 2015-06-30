import sys

from classes import Task, Group
from helpers import get_calling_module

__all__ = ['task', 'arg', 'group', 'module']

# Decorators
def task(Func=None, **Config):
  """A decorator to make tasks out of functions."""
  def decorator(Func):
    _Task = _wrapObject(Func, Task)
    _Task.Config.update(**Config)
    _Task.__prepare__()
    
    return _Task.Underlying
    
  return decorator(Func) if Func else decorator

def arg(name, **Config):
  """A decorator to configure an argument of a task.
  
    * It always follows a @task or an @arg.
  """
  def decorator(Func):
    _Task = _wrapObject(Func, Task)
    _Task.Args.insert(0, (name, Config))
    
    return _Task
    
  return decorator
  
def group(Underlying=None, **Config):
  """A decorator to make groups out of classes."""
  def decorator(Underlying):
    _Group = Group(Underlying)
    _Group.Config.update(**Config)
    
    return _Group.Underlying
    
  return decorator(Underlying) if Underlying else decorator

# Methods
def module(**Config):
  """Helps with adding configs to Modules.
  """
  Underlying = get_calling_module()
  _Group = Group(Underlying)
  _Group.Config.update(**Config)
  
  
# Helpers
def _wrapObject(Obj, Wrapper):
  return Obj if isinstance(Obj, Wrapper) else Wrapper(Obj)
  