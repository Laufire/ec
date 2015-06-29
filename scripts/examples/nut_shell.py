"""nut_shell - everything about using private.
==============================================
Notes
-----
* The decorators task, arg and group are available as __builtins__, when the script is launched using private.

* DocStrings of the tasks could be used by external modules (like sphinx). This is one of the key factors of developing private, apart from it's predecessor Commander.
"""

__config__ = {'desc': 'A module to test decorator based configuration.'} # __config__ is an attribute used by private as the Configuration store for groups (both modules and classes).

from private.modules.decorators import task, arg, group # though the imports are available as builtins, they have to be explicitly added for sphinx-autodoc to work

@task
@arg('arg1', type=int, desc='A description for the arg.')
@arg('arg2', type=int)
def task1(arg1, arg3=3, arg2=2):
  """A simple task, at the root of the script.
    * Note that the order of input collection will follow the order of configuration (in this case arg1, then arg2 and then arg3).
    * Any unconfigured arg will be collected after the collection of the configured args.
    * Since a name isn't specified in @task, the name of the task, *task1* will be used to identify this task.
  """
  print arg1, arg2, arg3

@group(desc = 'Description for group1.')
class group1:
  """A group
  Groups can contain tasks and other groups within them.
  """
  @task(name='task1')
  @arg('arg1', desc='Some string.')
  def _task1(arg1):
    """A task within a group.
      * Notice the missing **self** arg.
      * @task.name, *task1* will be the name of this task.
    """
    print arg1 + arg1
    