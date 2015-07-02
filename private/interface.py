import shlex

from modules.core import BaseGroup, execCommand, resolveMember

__all__ = ['resolve', 'call']

def resolve(route):
  """Resolves the member identified by the route."""
  return resolveMember(BaseGroup, shlex.split(route))
  
def call(route, collect_missing=False):
  """Calls a taskm as if it were called from the command line."""
  return execCommand(shlex.split(route), collect_missing)