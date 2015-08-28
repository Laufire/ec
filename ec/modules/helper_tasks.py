r"""
Helpers tasks for the shell mode.
"""
import os
import sys

from ec.ec import task, arg, group, module

from state import Settings
import core
from core import processModule
from helpers import err, getRouteHelp

module(desc='Shell mode Tasks.')

# Tasks
@task(alias='c', desc='Clears the console.')
def clear():
  r"""Clears the console.
  """
  os.system('cls' if os.name == 'nt' else 'clear')

@task(alias='h', desc='Displays help on the available tasks and groups.')
def help(route):
  r"""Displays help for the given route.

  Args:
    route (str): A route that resolves a member.
  """
  help_text = getRouteHelp(route.split('/') if route else [])

  if help_text is None:
    err('Can\'t help :(')

  else:
    print '\n%s' % help_text

# Main
def main():
  ThisModule = sys.modules[__name__]
  core.processModule(__name__)

  __ec_member__ = ThisModule.__ec_member__

  helper_route = Settings.get('helper_route')

  if helper_route:
    __ec_member__.Config['name'] = helper_route
    core.BaseGroup.Members[helper_route] = __ec_member__

  else:
    core.BaseGroup.Members.update(__ec_member__.Members.iteritems())
