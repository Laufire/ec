r"""
delegate
========

A module to help with making shared calls.
"""
from urllib import unquote
from json import dumps, loads

from ec.ec import task, arg

#State
sharedBase = 'shared'

def setSharedBase(name):
  global sharedBase

  sharedBase = name

# Tasks
@task(alias='mc')
@arg()
@arg()
def makeCall(callPath, argStr='[]'):
  Parts = callPath.split('/')
  scriptName = Parts.pop(0)

  Cursor = __import__(sharedBase + '.' + scriptName, fromlist=[scriptName]) # Start with the module.

  # #Pending: Think of loading nested modules, not just attibutes.

  for attr in Parts:
    Cursor = getattr(Cursor, attr) # Retrive the nested attributes.

  Args = loads(unquote(argStr))

  print dumps(Cursor(*Args) or {})
