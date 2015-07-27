"""
An example for using lambdas / functions as custom types.
"""
from ec.ec import task, arg
from ec.utils import custom

@task
@arg(type=custom(lambda v: v%2==1, 'an odd number', int))
def task1(arg1):
  print arg1
  