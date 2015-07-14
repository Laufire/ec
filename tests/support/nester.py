"""
nester
======

Used to test nested modules.
"""
from ec.ec import member, task

import target_script

member(target_script) # add the imported member to the script

@task
def task1():
  print 'task1'
  