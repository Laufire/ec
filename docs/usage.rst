Usage
========

Command line
-------------

To enter shell mode

.. code-block:: bash

  $ python script_path
  
To dispatch commands

.. code-block:: bash

  $ python script groupX/taskX [arg1=value arg2=value ...] # execute a task
  
  $ python script -p groupX/taskX arg1=value # execute a task, with partial args.
  
To launch a scriptlet/dir

.. code-block:: bash

  $ ec scriptlet/dir [flag] groupX/taskX [args ...]
  
Examples
---------
A simple example
################
.. literalinclude:: ../scripts/examples/simple.py
  :linenos:
  :language: python

From the command line enter

.. code-block:: bash

  $ python simple.py task1 arg1=1 arg2=2
    1 2
    
  $ python simple.py group1/task1 arg1=1
    2
    
    
An advanced example (wrapping ec to extend it)
####################################################
.. literalinclude:: ../scripts/examples/advanced/wrapping.py
  :linenos:
  :language: python

A nut shell example
###################
.. literalinclude:: ../scripts/examples/nut_shell.py
  :linenos:
  :language: python

Documentation of nut_shell.py
+++++++++++++++++++++++++++++
.. automodule:: nut_shell
    :members:
    :undoc-members:
    :show-inheritance:
