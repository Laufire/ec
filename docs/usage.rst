Usage
========

To use private from command line

**shell** mode

  $ python script_path
  
**dispatch** mode
  
    $ python script <command route> [arg1=value arg2=value ...] # execute a task
    
    $ python script -p <command route> arg1=value # execute a task, with partial args.
  
To launch a scriptlet/dir::

  $ private scriptlet/dir [flags] <command route> [args]
  
To use private in a project::

    import private
    
    private.members(...)
    
    private.call('<command route> [options]')


.. automodule:: nut_shell
    :members:
    :undoc-members:
    :show-inheritance:
