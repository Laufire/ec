"""Helper import for demonstrating advanced examples.
"""

from ec.ec import task, arg, group

@task
@arg('arg1', type=int, desc='Value for arg1 (int)')
@arg('arg2', type=int)
def task1(arg1, arg2=1):
  print arg1, arg2

@group(desc='Description for group1.')
class group1:
  @task
  @arg('arg1')
  def task1(arg1):
    print arg1 + arg1
