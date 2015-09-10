from ec.ec import task, arg

from ec.types.regex import pattern, email
from ec.types.multi import one_of
from ec.types.num import between
from ec.types.basics import yn

class types: # the class acts as a namespace to hide the task types from the user
  @task(desc='movie')
  def movie(name, rating=None):
    return '%s%s' % (name, ', rated %s.' % rating if rating is not None else '')

@task
@arg('id', type=pattern('^a.+'), desc='User id')
@arg('email_id', type=email, desc='email')
@arg('gender', type=one_of(['m', 'f']))
@arg('age', type=between(0, 150), desc='Age')
@arg('is_married', type=yn())
def add(id, email_id, gender, age, is_married):
  print id, email_id, gender, age, is_married


from ec.types.adv import invert
@task(alias='t')
@arg(type=invert(int))
def t(arg):
  "A task to test the custom type under development."
  print arg
