ec
===

ec - the simplest way to create CLI applications.

* Free software: MIT license
  
A simple example
-----------------
from: `simple.py <https://github.com/Laufire/ec/blob/master/scripts/examples/simple.py>`_

.. code:: python
  
  from ec.ec import task, arg, group

  @task # define a task
  @arg(type=int, desc= 'Value for arg1') # add an argument with a type and a description
  @arg(type=int)
  def task1(arg1, arg2=1):
    print arg1, arg2

  @group(desc = 'A group with some tasks') # define a group
  class group1:
    @task
    def task1(arg1): # define a task inside the group
      print arg1 + arg1

**Execute a task:** *<dispatch mode>*

From the command-line enter

.. code:: bash

  $ python simple.py task1 arg1=1 arg2=2
    1 2
    
  $ python simple.py group1/task1 arg1=1
    2
    
**Interactively execute tasks:** *<shell mode>*

From the command-line enter

.. code:: bash

  $ python simple.py # this will enter into ec-shell
	
	>task1
	Value for arg1: 1
	arg2 (1): 2
	1 2
	
	>group1/task1 # execute task1 under group1
	arg1: 1
	11
	
	>task1 arg1=1 # arguments can be given while calling the task, the missing arguments will be collected from the user
	arg2 (1): 2
	1 2
	
	>^Z # exit the shell


Detailed docs could be found at `PyDocs <http://pythonhosted.org/ec/>`_.
