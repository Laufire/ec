"""
All the classes of ec.
"""
from collections import OrderedDict

class Member():
  """The base class for the classes Task and Group.
  
    It brands the given underlying with the __ec_member__ attr, which is used to identify the Underlying as processable by ec.
  """
  def __init__(self, Underlying, Config):
    __ec_member__ = getattr(Underlying, '__ec_member__', None)
    
    if __ec_member__:
      __ec_member__.Config.update(Config)
      self.Config = __ec_member__.Config
      
    else:
      Underlying.__ec_member__ = self
      self.Config = Config
      
    self.Underlying = Underlying

class Task(Member):
  """A callable class that allows the calling of the underlying function as a task.
  """
  def __init__(self, Underlying, Args, Config=None):
    
    if Config is None:
      Config = {}
      
    if not 'name' in Config:
      Config['name'] = Underlying.func_name.rsplit('.', 1)[-1]
      
    Member.__init__(self, Underlying, Config)
    
    self.Args = self.__load_args__(Args)
    
  def __load_args__(self, Args):
    """Prepares the task for excecution.
    """
    FuncArgs = _getFuncArgs(self.Underlying)
    
    OrderedArgs = OrderedDict() # Note: the order of configuration (through decorators) is prefered over the order of declaration (within the function body)
    
    for Arg in Args:
      argName = Arg.get('name')
      
      if argName is None:
        if not FuncArgs:
          raise HandledException('Excess args while configuring "%s".' % self.Config['name'])
          
        FuncArg = FuncArgs.iteritems().next() # get the next free arg
        argName = FuncArg[0]
        FuncArg = FuncArg[1]
        
      else:
        FuncArg = FuncArgs.get(argName)
        
        if FuncArg is None:
          raise HandledException('Unknown arg "%s" while configuring "%s".' % (argName, self.Config['name']))
          
      FuncArg.update(Arg) # prefer Args config over the values given while defining the function.
      OrderedArgs[argName] = FuncArg
      del FuncArgs[argName]
      
    OrderedArgs.update(FuncArgs.iteritems()) # add any unconfigured args
    
    return OrderedArgs
    
  def __get_arg__(self, argName):
    """Gets user input for a single arg.
    """
    Arg = self.Args[argName]
    ArgOptions = Arg.copy()
    
    if 'desc' in Arg:
      ArgOptions['autoDesc'] = False
      
    else:
      ArgOptions['desc'] = self.__get_arg__desc__(argName)
      
    return get(**ArgOptions)
    
  def __get_arg__desc__(self, argName):
    """Generates a description for the input; 'argName' or 'argName (default) will be the description.
    """
    Arg = self.Args[argName]
    _type = Arg.get('type')
    
    return '%s (%s)' % (argName, Arg['default']) if 'default' in Arg else argName
    
  def __confirm_known_args__(self, InArgs):
    """Confirms that only known args are passed to the underlying.
    """
    ArgKeys = self.Args.keys()
    
    for k in InArgs.keys():
      if k not in ArgKeys:
        raise HandledException('Unknown arg: %s.' % k, Member=self)
  
  def __digest_args__(self, InArgs, InKwArgs):
    """Digests the given Args and KwArgs and return a singele KwArgs dictionary.
    """
    KwArgs = {}
    ArgKeys = self.Args.keys()
    
    for arg in InArgs:
      key = ArgKeys.pop(0)
      
      if key in InKwArgs:
        raise HandledException('Multiple assignments for the arg "%s".' % key)
        
      KwArgs[key] = arg
    
    KwArgs.update(InKwArgs)
    
    self.__confirm_known_args__(KwArgs)
    
    return KwArgs
  
  def __call__(self, *InArgs, **InKwArgs):
    
    KwArgs = self.__digest_args__(InArgs, InKwArgs)
    
    for name, Arg in self.Args.items():
      _type = Arg.get('type')
      
      if not name in KwArgs:
        if 'default' in Arg:
           default = Arg['default']
          
        elif hasattr(_type, 'default'):
          default = _type.default
          
        else:
          raise HandledException('Missing argument: %s.' % name, Member=self)
        
        KwArgs[name] = default
        
      else:
        if _type:
          try:
            KwArgs[name] = _type(KwArgs[name])
            
          except (ValueError, TypeError):
            raise HandledException('Invalid value for "%s", expected %s; got "%s".' % (name, _type, KwArgs[name]), help_type='task', Member=self)
    
    return self.Underlying(**KwArgs)
  
  def __collect_n_call__(self, *InArgs, **InKwArgs):
    """Helps with collecting all the args and call the Task.
    """
    KwArgs = self.__digest_args__(InArgs, InKwArgs)
    
    for name, Arg in self.Args.items():
      if not name in KwArgs:
        KwArgs[name] = self.__get_arg__(name)
        
      else:
        _type = Arg.get('type')
        try:
          KwArgs[name] = _type(KwArgs[name]) if _type else KwArgs[name]
          
        except (ValueError, TypeError):
          KwArgs[name] = self.__get_arg__(name)
      
    return self.Underlying(**KwArgs)
    
class Group(Member):
  """Groups can contain other Members (Tasks / Groups).
  
  Note:
    Groups that have modules as their underlying would have it's members loaded by ec.start.
  """
  def __init__(self, Underlying, Config=None):
    if Config is None:
      Config = {}
    
    if not 'name' in Config:
      Config['name'] = Underlying.__name__.rsplit('.', 1)[-1]
    
    Member.__init__(self, Underlying, Config or {})
    
class CustomType:
  """The base class for custom types.
  """  
  def __init__(self, desc=None):
    if desc is not None:
      self.desc = desc
  
  def __str__(self):
    """Used to represent the type as a string, in messages and queries."""
    return getattr(self, 'desc', 'custom type')
    
# Helper Classes
class HandledException(Exception):
  """A custom error class for ec's interanl exceptions, which are handled within ec.
  """
  
  def __init__(self, e, **Info):
    self.Info = Info
    super(HandledException, self).__init__(getattr(e, 'message', e))

# Helpers
def _getFuncArgs(func):
  """Gives the details on the args of the given func.
  
  Args:
    func (function): The function to get details on.
  """
  code = func.func_code
  Defaults = func.func_defaults
  
  nargs = code.co_argcount
  ArgNames = code.co_varnames[:nargs]
  
  Args = OrderedDict()
  argCount = len(ArgNames)
  defCount = len(Defaults) if Defaults else 0
  diff = argCount - defCount
  
  for i in range(0, diff):
    Args[ArgNames[i]] = {}
    
  for i in range(diff, argCount):
    Args[ArgNames[i]] = {'default': Defaults[i - diff]}
    
  return Args
  
# Cross dependencies
from exposed import get, static
from helpers import err, ismodule
