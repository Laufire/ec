import sys

from classes import Task, Group

__all__ = ['task', 'arg', 'group']

# Decorators
def task(Func=None, **Config):
  def decorator(Func):
    _Task = _wrapObject(Func, Task)
    _Task.Config.update(**Config)
    _Task.__prepare__()
    
    return _Task
    
  return decorator(Func) if Func else decorator

def arg(name, **Config):
  def decorator(Func):
    _Task = _wrapObject(Func, Task)
    _Task.Args.insert(0, (name, Config))
    
    return _Task
    
  return decorator
  
def group(Underlying=None, **Config):
  def decorator(Underlying):
    _Group = Group(Underlying)
    _Group.Config.update(**Config)
    
    return _Group
    
  return decorator(Underlying) if Underlying else decorator
  
# Helpers
def _wrapObject(Obj, Wrapper):
  return Obj if isinstance(Obj, Wrapper) else Wrapper(Obj)
  