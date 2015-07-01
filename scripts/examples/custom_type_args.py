from private.private import start, task, arg, group

from private.types.regex import pattern, email
from private.types.multi import some_of
from private.types.num import between

@task
@arg('id', type=pattern('^a.+'), desc='User id')
@arg('email_id', type=email, desc='email')
@arg('colors', type=some_of(['r', 'g', 'b']), desc='Colors; some of r, g, b')
@arg('age', type=between(0, 150), desc='Age')
def add(id, email_id, colors, age):
  print id, email_id, colors, age

start()