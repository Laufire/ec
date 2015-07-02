import os

from ec.ec import task, arg, group, module

from core import resolveMember, BaseGroup
from classes import Group, Task
from helpers import err

# Helper Exports
def list_members(route=''):
  
  Ret = []
  TargetGroup = resolveMember(BaseGroup, route.split(' ')) if route else BaseGroup
  
  for name, Member in TargetGroup.Config['Members'].items():
    Ret.append((name, Member.Config.get('desc', '')))
  
  return Ret
  
# Tasks
@task
def clear():
	os.system('cls' if os.name == 'nt' else 'clear')
  
@task
def help(route):
  Resolved = resolveMember(BaseGroup, route.split(' ')) if route else BaseGroup
  
  if isinstance(Resolved, Group):
    print '\n'.join([('%s  %s' % (name, desc))[:60] for name, desc in list_members(route)])
    
  elif isinstance(Resolved, Task):
    print _getTaskHelp(Resolved)
    
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
    Ret.append('Args:')
    Props = ['name', 'desc', 'type', 'default']
    
    for argName, Arg in Args.items():
      Ret.append('  name: %s' % argName)
      
      for k in Props:
        v = Arg.get(k)
        
        if v is not None:
          Ret.append('  %s: %s' % (k, v))
      
      Ret.append('')
    Ret.pop()
    
  return '\n'.join(Ret)
  