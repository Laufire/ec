import shlex

from modules import core
from modules.core import execCommand, resolveMember

__all__ = ['resolve', 'call']

def resolve(route):
  """Resolves the member identified by the route."""
  return resolveMember(core.BaseGroup, shlex.split(route))
  
def call(route, collect_missing=False):
  """Calls a task, as if it were called from the command line."""
  return execCommand(shlex.split(route), collect_missing)