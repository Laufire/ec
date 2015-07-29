"""
allied
======

A script to test allied features.
"""
from ec.ec import task, arg, group, call, module, settings, exit_hook

@task(alias='t1')
def task1(arg1):
  return arg1

@exit_hook
def exit_handler():
  print str(range(1, 10)) # a signature output for verification
