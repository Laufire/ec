"""
target_script
=============

The target for testing.
"""
from ec.ec import task, arg, group, settings

@task(alias='t1')
@arg(type=int, desc= 'Value for arg1')
@arg('arg2', type=int)
def task1(arg1, arg3=3, arg2=2):
  print arg1, arg2
  return arg1, arg2

@group(desc = 'Description for group1')
class group1:
	@task
	@arg('arg1')
	def task1(arg1):
		print arg1
