"""
Helpers tasks for the shell mode.
"""
import os
import sys

from ec.ec import task, arg, group, module

from state import Settings
import core
from core import getDescendant, processModule
from classes import Group, Task
from helpers import err, listMemberHelps

module(desc= 'Shell mode Tasks.')

# Tasks
@task(alias='c', desc='Clears the console.')
def clear():
  """Clears the console.
  """
  os.system('cls' if os.name == 'nt' else 'clear')
  
@task(alias='h', desc='Displays help on the available tasks and groups.')
def help(member):
  """Displays help for the given member.
  
  Args:
    member (str): A route that resolves a member.
  """
  Resolved = getDescendant(core.BaseGroup, member.split(' ')) if member else core.BaseGroup
  
  if isinstance(Resolved, Group):
    return '\n%s\n' % '\n\n'.join([('%s  %s' % (name, desc))[:60] for name, desc in listMemberHelps(Resolved)])
    
  elif isinstance(Resolved, Task):
    return '\n%s\n' % _getTaskHelp(Resolved)
    
  else:
    err('Can\'t help :(')
    
# Main
def main():
  __ec_member__ = sys.modules[__name__].__ec_member__
  
  helper_route = Settings.get('helper_route')
  
  if helper_route:
    __ec_member__.Config['name'] = helper_route
    core.BaseGroup.Config['Members'][helper_route] = __ec_member__
    
  else:
    core.BaseGroup.Config['Members'].update(__ec_member__.Config['Members'].iteritems())

# Helpers
def _getTaskHelp(_Task):
  Ret = []
  
  for k in ['name', 'desc']:
    v = _Task.Config.get(k)
    
    if v is not None:
      Ret.append('%s: %s' % (k, v))
  
  Args = _Task.Args
  
  if Args:
    Ret.append('\nArgs:')
    Props = ['desc', 'type', 'default']
    
    for argName, Arg in Args.items():
      Ret.append('  name: %s' % argName)
      
      for k in Props:
        v = Arg.get(k)
        
        if v is not None:
          Ret.append('  %s: %s' % (k, v))
      
      Ret.append('')
      
    Ret.pop()
    
  return '\n'.join(Ret)
  