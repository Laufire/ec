from private.private import start, task, arg, group

from private.types.regex import pattern, email
from private.types.multi import one_of
from private.types.num import between
from private.types.basics import yn
from private.types.adv import t2t

@task
@arg('id', type=pattern('^a.+'), desc='User id')
@arg('email_id', type=email, desc='email')
@arg('gender', type=one_of(['m', 'f']))
@arg('age', type=between(0, 150), desc='Age')
@arg('is_married', type=yn())
def add(id, email_id, gender, age, is_married):
  print id, email_id, gender, age, is_married

class types: # the class acts as a namespace to hide the task types from the user
  @task(desc='movie')
  def movie(name, rating=None):
    return '%s%s' % (name, ', rated %s.' % rating if rating is not None else '')

@task
@arg('arg', type=t2t(types.movie))
def t(arg):
  print arg
  
start()