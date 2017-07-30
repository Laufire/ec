from ec.ec import task, arg, group

@task # define a task
@arg(type=int, desc='Value for arg1') # add an argument with a type and a description
@arg(type=int)
def task1(arg1, arg2=1):
  print arg1 + arg2

@group(desc='A group with some tasks') # define a group
class group1:
  @task
  def task1(arg1): # define a task inside the group
    print arg1 + arg1
