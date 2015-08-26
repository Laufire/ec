r"""
simple
======

A simple testing target script.
"""
from ec.ec import task, arg, group, call, module, settings

@task(alias='t1')
@arg(type=int, desc='Value for arg1')
@arg('arg2', type=int)
def task1(arg1, arg3=3, arg2=2): #pylint: disable=W0613
  print arg1, arg2
  return arg1, arg2

@group(desc='Description for group1')
class group1:
  @task
  @arg('arg1')
  def task1(arg1):
    print arg1
    return 1

@task(desc='Throws an exception')
def ex():
  1 / 0 #pylint: disable=W0104
  
@task(desc='Throws a handled exception')
def hex():
  task1.__ec_member__.__call__(arg1='a') # a handled exception would be raised because of mismatched type.
  
# settings(dev_mode=True) # shortcut: enable the line to get the stack trace on exceptions
