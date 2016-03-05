r"""
Everything about using ec. this module is designed to be a nut shell guide to ec and as a way to enable test driven development.

Notes
-----
* The decorators task, arg and group are available as __builtins__, when the script is launched using ec.
* DocStrings of the tasks could be used by external modules (like sphinx). This is one of the key factors of developing ec, apart from it's predecessor Commander.
"""
from ec.ec import task, arg, group, module, member, call, settings, exit_hook, throw
from ec.utils import get
from ec.types import regex

@task
@arg(type=int, desc='Some int') # configure the first arg
@arg('arg2', type=int) # configure the arg named 'arg2'.
def task1(arg1, arg3=3, arg2=2):
  r"""A simple task, at the root of the script.

    * Note that the order of input collection will follow the order of configuration (in this case arg1 and then arg2).
    * Any unconfigured args will be collected after the collection of the configured args (hence arg3 will be collected as the last arg).
    * Since a name isn't specified in @task, the name of the task, *simple* will be used as the name of this task.
  """
  print arg1, arg2, arg3

@group(alias='i', desc='A group.')
class intro:
  r"""
    Groups can contain tasks and other groups within them.
    This group has an alias; thus could be identified as **intro** or **i**. Tasks to could have aliases.
  """
  @task(name='simple')
  @arg('arg1', desc='Some string')
  def renamed_task(arg1):
    r"""A task within a group.

      * This task can be accessed as intro/simple.
      * Notice the missing **self** arg.
      * @task.name, **simple** will be the name of this task, not the function name **renamed_task**.
    """
    intro.log('%s, from %s.' % (arg1, intro.name))

  @task
  def wrapper():
    r"""Calls nut_shell.simple with some arguments, the args that aren't provided will be collected.
    """
    call(simple, arg1=1, arg2=2)

  @task
  def get():
    r"""Get user input through utils.get.
    """
    print get(desc='Email id', type=regex.email)

  def log(message):
    r"""A helper method.
    """
    print message

  name = 'intro' # Groups could even have variables.

@task
@arg(type=lambda v: (int(v) if int(v) > 10 else throw()), desc='Some int', type_str='a number greater than 10') # a lambda as a custom type
def task2(arg1):
  print arg1

# importing other modules
import simple
member(simple) # member() is used to expose imported members as the children of the current module

@exit_hook
def clean_up(): # exit hooks are called when ec exits. There may be more than one hook.
  print ':)'

module(desc='A module to test decorator based configuration.') # module is an optional call, used to configure the group that wraps current module.

settings(dev_mode=True) # settings for ec
