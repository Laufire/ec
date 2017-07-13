r"""
A script to inject the delegator script to the calling module.
"""
def inject(sharedBase=None, **Settings):

  import sys
  from json import dumps
  from urllib import quote

  from ec import interface
  from ec.ec import settings

  import delegator # #Note: An ec module is used, instead of making the call directly, so to utilize ec's features like debugging etc.

  if sharedBase:
    delegator.setSharedBase(sharedBase)

  if Settings:
    settings(**Settings)

  Args = sys.argv[1:]

  interface.setBase(delegator)
  interface.call('makeCall %s %s' % (Args[0], quote(dumps(Args[1:]))), silent=False)
  # #Note: Debugging is allowed.
  # #Note: Quoted JSON is used, as Python 2 doesn't have a shlex.quote.
