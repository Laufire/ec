"""
nut_shell
=========
  Everything about using ec: this module is designed to be a nut shell guide to ec and as a way to enable test driven development.
  
Notes
-----
* The decorators task, arg and group are available as __builtins__, when the script is launched using ec.
* DocStrings of the tasks could be used by external modules (like sphinx). This is one of the key factors of developing ec, apart from it's predecessor Commander.
"""

from ec.ec import start, task, arg, group, module, call
from ec.utils import get
from ec.types import regex

@task
@arg('arg1', type=int, desc='Some int')
@arg('arg2', type=int)
def simple(arg1, arg3=3, arg2=2):
  """A simple task, at the root of the script.
  
    * Note that the order of input collection will follow the order of configuration (in this case arg1 and then arg2).
    * Any unconfigured arg will be collected after the collection of the configured args (hence arg3 will be collected as the last arg).
    * Since a name isn't specified in @task, the name of the task, *simple* will be used as the name of this task.
  """
  print arg1, arg2, arg3

@group(alias='i', desc = 'Description for group1.')
class intro:
  """A group.
  
    Groups can contain tasks and other groups within them.
    This group has an alias; thus could be identified as **intro** or **i**. Tasks to could have aliases.
  """
  @task(name='simple')
  @arg('arg1', desc='Some string')
  def renamed_task(arg1):
    """A task within a group.
    
      * This task can be accessed as intro/simple.
      * Notice the missing **self** arg.
      * @task.name, **simple** will be the name of this task, not the function name **renamed_task**.
    """
    intro.log('%s, from %s.' % (arg1, intro.name))
    
  @task
  def wrapper():
    """Calls nut_shell.simple with some arguments, the args that aren't provided will be collected."""
    call(simple, arg1=1, arg2=2)
    
  @task
  def get():
    """Get user input through utils.get."""
    print get(desc='Email id', type=regex.email)
    
  @staticmethod
  def log(message):
    """Helper methods, are intended to help the tasks. They are often declared as static methods, due to them being members of unintantiated classes.
    """
    print message
    
  name = 'intro' #: Groups could even have ec variables.
  
module(desc='A module to test decorator based configuration.') # module is an optional call, used to configure the group that wraps current module.

start()