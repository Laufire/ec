r"""
Provides the decorators and functions for the configuration of the args, tasks, groups and modules.
"""
import sys

import state
from state import Settings, ExitHooks
from classes import Task, Group, HandledException
from helpers import getCallingModule
from helpers import isclass
from exposed import static
__all__ = ['task', 'arg', 'group', 'module']

# Helpers
def wrap(func, with_func): # Check: Is wrapping of the decorator needed? They seem to be unnecesary.
  r"""Copies the function signature from the wrapped function to the wrapping function.
  """
  func.__name__ = with_func.__name__
  func.__doc__ = with_func.__doc__
  func.__dict__.update(with_func.__dict__)
  
  return func

def decorator(func):
  r"""Makes the passed decorators to support optional args.
  """
  def wrapper(__decorated__=None, *Args, **KwArgs):
    if __decorated__ is None: # some args is available through the decorator
      return lambda _func: func(_func, *Args, **KwArgs)
      
    else:
      return func(__decorated__, *Args, **KwArgs)
    
  return wrap(wrapper, func)

# Decorators
@decorator
def task(__decorated__=None, **Config):
  r"""A decorator to make tasks out of functions.
  
  Config:
    * name (str): The name of the task. Defaults to __decorated__.__name__.
    * desc (str): The description of the task (optional).
    * alias (str): The alias for the task (optional).
  """
  if isinstance(__decorated__, tuple):  # the task has some args
    _Task = Task(__decorated__[0], __decorated__[1], Config=Config)
  
  else:
    _Task = Task(__decorated__, [], Config)
  
  state.ActiveModuleMemberQ.insert(0, _Task)
  
  return _Task.Underlying

def arg(name=None, **Config): # wraps the _arg decorator, in order to allow unnamed args
  r"""A decorator to configure an argument of a task.
  
  Config:
    * name (str): The name of the arg. When ommited the agument will be identified through the order of configuration.
    * desc (str): The description of the arg (optional).
    * type (type, CustomType, callable): The alias for the task (optional).
    
  Notes:
    * It always follows a @task or an @arg.
  """
  if name is not None: # allow name as a positional arg
    Config['name'] = name
    
  return lambda decorated: _arg(decorated, **Config)

@decorator
def _arg(__decorated__, **Config):
  r"""The worker for the arg decorator.
  """
  if isinstance(__decorated__, tuple):  # this decorator is followed by another arg decorator
    __decorated__[1].insert(0, Config)
    return __decorated__
    
  else:
    return __decorated__, [Config] # this decorator is the first arg decorator
  
@decorator
def group(__decorated__, **Config):
  r"""A decorator to make groups out of classes.
  
  Config:
    * name (str): The name of the group. Defaults to __decorated__.__name__.
    * desc (str): The description of the group (optional).
    * alias (str): The alias for the group (optional).
  """
  _Group = Group(__decorated__, Config)
  
  if isclass(__decorated__): # conver the method of the class to static methods so that they could be accessed like object methods; ir: g1/t1(...).
    static(__decorated__)
    
  state.ActiveModuleMemberQ.insert(0, _Group)
  
  return _Group.Underlying

@decorator
def exit_hook(callable, once=True):
  r"""A decorator that makes the decorated function to run while ec exits.
  
  Args:
    callable (callable): The target callable.
    once (bool): Avoids adding a func to the hooks, if it has been added already. Defaults to True.
    
  Note:
    Hooks are processedd in a LIFO order.
  """
  if once and callable in ExitHooks:
    return
    
  ExitHooks.append(callable)
  

# Methods
def module(**Config):
  r"""Helps with adding configs to Modules.
  
  Note:
    Config is a same as that of **group**.
  """
  Underlying = getCallingModule()
  Underlying.__ec_member__.Config.update(**Config)
  
def member(Imported, **Config):
  r"""Helps with adding imported members to Scripts.
  
  Note:
    Config depends upon the Imported. It could be that of a **task** or a **group**.
  """
  __ec_member__ = Imported.__ec_member__
  __ec_member__.Config.update(**Config)
  
  state.ActiveModuleMemberQ.insert(0, __ec_member__)
  