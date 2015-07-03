from collections import OrderedDict

from helpers import err

class Member: # the base class for the classes group and task
  """
  The base class for the classes Task and Group
    Brands the given underlying with the __ec_member__ attr, which is used to identify the Underlying as processable by ec.
  """
  def __init__(self, Underlying, Config):
    Underlying.__ec_member__ = self
    self.Underlying = Underlying
    self.Config = Config
    
class Task(Member):
  """A callable class that allows the calling of the underlying function as a task."""
  def __init__(self, Underlying, Args, Config):
    
    if not 'name' in Config:
      Config['name'] = Underlying.func_name
      
    Member.__init__(self, Underlying, Config)
    
    try:
      self.__load_args__(Args)
    
    except HandledException as e:
      err(e, 1)
      
  def __call__(self, **Args):    
    self.__digest__(Args)
    try:
      return self.Underlying(**Args)
      
    except TypeError as e:
      raise HandledException(e)
  
  def __load_args__(self, Args):
    """Prepares the task for excecution."""
    FuncArgs = getFuncArgs(self.Underlying)
    OrderedArgs = OrderedDict() # the order of configuration (through decorators) is prefered over the order of declaration (within the function body)
    
    for Arg in Args:
      argName = Arg['name']
      FuncArg = FuncArgs.get(argName)
      if FuncArg is not None:
        FuncArg.update(**Arg) # prefer Args config over the values given while defining the function.
        Arg = FuncArg
        del FuncArgs[argName]
        
      else:
        raise HandledException('Unknown arg "%s" while configuring "%s".' % (k, self.Config['name']))
        
      OrderedArgs[argName] = Arg
      
    OrderedArgs.update(FuncArgs.iteritems())
    
    self.Args = OrderedArgs
    
  def __digest__(self, InArgs):
    """A helper for __call__ that digests the provided Args"""
    self.__confirm_known_args__(InArgs)
    
    for name, Arg in self.Args.items():
      if not name in InArgs:
        if 'default' in Arg:
          InArgs[name] = Arg['default']
          
        else:
          raise HandledException('Missing argument: %s.' % name)
        
      else:
        _type = Arg.get('type')
        if _type:
          try:
            InArgs[name] = _type(InArgs[name])
            
          except ValueError:
            raise HandledException('Invalid value for "%s", expected %s; got "%s".' % (name, _type, InArgs[name]))
      
  def __collect_arg__(self, argName):
    """Collects a single arg."""
    Arg = self.Args[argName]
    _type = Arg.get('type')
    desc = desc = Arg.get('desc', self.__get_arg__desc__(argName))
    
    while True:
      try:
        line = raw_input('%s: ' % desc)
        
        if not line:
          if 'default' in Arg:
            return Arg['default']
        
        input = line
        
      except EOFError: # consider ^z as None
      
        input = None
        
      try:
        return _type(input) if _type else input
        
      except ValueError:
        err('<invalid value>')
        
      except TypeError:
        err('<invalid value>')
    
  def __get_arg__desc__(self, argName):
    """
    Generates a description for the input, when 'desc' is not provided.
    Generation Order
    ----------------
    
    * When a **CustomType** with its own **desc** is available, the descriprion will be 'argName CustomType.desc'.
    * Else 'argName'  or 'argName (dfault) will be the description.
    """
    Arg = self.Args[argName]
    _type = Arg.get('type')
    
    if isinstance(_type, CustomType):
      return '%s, %s' % (argName, _type)
    
    return '%s (%s)' % (argName, Arg['default']) if 'default' in Arg else argName
    
  def __confirm_known_args__(self, InArgs):
    """Confirms that only known args are passed to the underlying."""
    ArgKeys = self.Args.keys()
    
    for k in InArgs.keys():
      if k not in ArgKeys:
        raise HandledException('Unknown arg: %s.' % k)
  
  def __collect_n_call__(self, **InArgs):
    """Helps with collecting all the args and call the Task.
    """
    self.__confirm_known_args__(InArgs)
    
    for name, Arg in self.Args.items():
      if not name in InArgs:
        InArgs[name] = self.__collect_arg__(name)
        
      else:
        _type = Arg.get('type')
        try:
          InArgs[name] = _type(InArgs[name]) if _type else InArgs[name]
          
        except ValueError:
          InArgs[name] = self.__collect_arg__(name)
      
    return self.Underlying(**InArgs)
    
class Group(Member):
  """Groups can contain other Members (Tasks / Groups)."""
  def __init__(self, Underlying, Config):
    if not 'name' in Config:
      Config['name'] = Underlying.__name__
    
    Member.__init__(self, Underlying, Config)
    
    self.Config['Members'] = Members = {}
    
    for Item in vars(Underlying).values(): # collect all the children (branded with __ec_member__)
      __ec_member__ = getattr(Item, '__ec_member__', None)
      if __ec_member__:
        Config = __ec_member__.Config
        Members[Config['name']] = __ec_member__
        if 'alias' in Config:
          Members[Config['alias']] = __ec_member__
    
class CustomType:
  def __init__(self, desc=None):
    if desc is not None:
      self.desc = desc
  
  def __str__(self):
    desc = getattr(self, 'desc', None)
    
    return desc or ''
    
# Helper Classes
class HandledException(Exception): # a custom error class for interanl exceptions, in order to differentiate them from the script raised exceptions

  def __init__(self, e, *args):
    self.args = args
    super(HandledException, self).__init__(getattr(e, 'message', e))

# Helpers
def getFuncArgs(func): # get details on the args of the given func
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
  