"""
Helpers tasks for the shell mode.
"""
import os

from ec.ec import task, arg, group, module

from core import getDescendant, BaseGroup
from classes import Group, Task
from helpers import err

# Helper Exports
def listMemberHelps(route=''):
  
  Members = []
  TargetGroup = getDescendant(BaseGroup, route.split(' ')) if route else BaseGroup
  
  for Member in TargetGroup.Config['Members'].values(): # get unique children (by discarding aliases)
    if Member not in Members:
      Members.append(Member)
    
  Ret = []
  
  for Member in Members:
    Config = Member.Config
    Ret.append(('%s%s' % (Config['name'], ', %s' % Config['alias'] if 'alias' in Config else ''), Config.get('desc', '')))
  
  return Ret
  
# Tasks
@task(alias='c', desc='Clears the console.')
def clear():
  os.system('cls' if os.name == 'nt' else 'clear')
  
@task(alias='h', desc='Displays help on the available tasks and groups.')
@arg(desc='item')
def help(route):
  Resolved = getDescendant(BaseGroup, route.split(' ')) if route else BaseGroup
  
  if isinstance(Resolved, Group):
    return '\n%s\n' % '\n\n'.join([('%s  %s' % (name, desc))[:60] for name, desc in listMemberHelps(route)])
    
  elif isinstance(Resolved, Task):
    return '\n%s\n' % _getTaskHelp(Resolved)
    
  else:
    err('Can\'t help :(')
    
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
  