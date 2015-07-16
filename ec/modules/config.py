"""
Provides the decorators and functions for the configuration of the args, tasks, groups and modules.
"""
import sys

import state
from state import Settings
from classes import Task, Group, HandledException
from helpers import getCallingModule
from helpers import isclass
from exposed import static
__all__ = ['task', 'arg', 'group', 'module']

# Helpers
def wrap(func, with_func): # Check: Is wrapping of the decorator needed? They seem to be unnecesary.
  """Copies the function signature from the wrapped function to the wrapping function.
  """
  func.__name__ = with_func.__name__
  func.__doc__ = with_func.__doc__
  func.__dict__.update(with_func.__dict__)
  
  return func

def decorator(func):
  """Makes the passed decorators to support optional args.
  """
  def wrapper(__decorated__=None, **Config):
    if __decorated__ is None: # some configration is available through the decorator
      return lambda _func: func(_func, **Config)
      
    else:
      return func(__decorated__, **Config)
    
  return wrap(wrapper, func)

# Decorators
@decorator
def task(__decorated__=None, **Config):
  """A decorator to make tasks out of functions.
  """
  if isinstance(__decorated__, tuple):  # the task has some args
    _Task = Task(__decorated__[0], __decorated__[1], Config=Config)
  
  else:
    _Task = Task(__decorated__, [], Config)
  
  state.ActiveModuleMemberQ.insert(0, _Task)
  
  return _Task.Underlying

def arg(name=None, **Config): # wraps the _arg decorator, in order to allow unnamed args
  """A decorator to configure an argument of a task.
  
  Notes:
    * It always follows a @task or an @arg.
  """
  if name is not None:
    Config['name'] = name
    
  return lambda decorated: _arg(decorated, **Config)

@decorator  
def _arg(__decorated__, **Config):
  """The worker for the arg decorator.
  """
  if isinstance(__decorated__, tuple):  # this decorator is followed by another arg decorator
    __decorated__[1].insert(0, Config)
    return __decorated__
    
  else:
    return __decorated__, [Config] # this decorator is the first arg decorator
  
@decorator
def group(Underlying, **Config):
  """A decorator to make groups out of classes.
  """
  _Group = Group(Underlying, Config)
  
  if isclass(Underlying): # conver the method of the class ro static methods so that they could be accessed like object methods; ir: g1/t1(...).
    static(Underlying)
    
  state.ActiveModuleMemberQ.insert(0, _Group)
  
  return _Group.Underlying
  
# Methods
def module(**Config):
  """Helps with adding configs to Modules.
  """
  Underlying = getCallingModule()
  Group(Underlying, Config)
  
def member(Imported, **Config):
  """Helps with adding imported members to Scripts.
  """
  __ec_member__ = Imported.__ec_member__
  __ec_member__.Config.update(**Config)
  
  state.ActiveModuleMemberQ.insert(0, __ec_member__)
  