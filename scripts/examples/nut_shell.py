"""
nut_shell
=========
  Everything about using private: this module is designed to be a nut shell guide to private and as a way to enable test driven development.
  
Notes
-----
* The decorators task, arg and group are available as __builtins__, when the script is launched using private.
* DocStrings of the tasks could be used by external modules (like sphinx). This is one of the key factors of developing private, apart from it's predecessor Commander.
"""

from private.private import start, task, arg, group, module

@task
@arg('arg1', type=int, desc='Some int')
@arg('arg2', type=int)
def task1(arg1, arg3=3, arg2=2):
  """A simple task, at the root of the script.
  
    * Note that the order of input collection will follow the order of configuration (in this case arg1 and then arg2).
    * Any unconfigured arg will be collected after the collection of the configured args (hence arg3 will be collected as the last arg).
    * Since a name isn't specified in @task, the name of the task, *task1* will be used as the name of this task.
  """
  print arg1, arg2, arg3

@group(desc = 'Description for group1.')
class group1:
  """A group.
  
    Groups can contain tasks and other groups within them.
    A **class** is used as a namespace for the group.
  """
  @task(name='task1')
  @arg('arg1', desc='Some string.')
  def task_1(arg1):
    """A task within a group.
    
      * Notice the missing **self** arg.
      * @task.name, **task1** will be the name of this task, not the function name **task_1**.
    """
    group1.log('%s, from %s.' % (arg1, group1.name))
    
  @staticmethod
  def log(message):
    """Helper methods, are intended to help the tasks. They are often decalred as static methods, due to them being members of unintantiated classes.
    """
    print message
    
  name = 'group1' #: Groups could even have private variables.
  
module(desc='A module to test decorator based configuration.') # module is an optional call, used to configure the current module.

start()