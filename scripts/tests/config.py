@task
def unconfigured(a, b=1):
  print a, b
  
@group(name='arg')
class _arg:
  @task
  @arg('a', type=int)
  def without_desc(a, b=1):
    print a, b