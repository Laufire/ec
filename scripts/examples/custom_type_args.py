from private.types.regex import pattern
from private.private import start, task, arg, group

@task
@arg('arg1', type=pattern('a.*'), desc= 'Some string that starts with an \'a\'.')
def task1(arg1):
  print arg1

start()