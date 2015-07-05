from ec.ec import start, task, arg

from ec.types.regex import email

@task
@arg('email_id', type=email, desc='email')
def add(email_id):
  print email_id
  
start()