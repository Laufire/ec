"""
All the classes of ec.
"""
from collections import OrderedDict

from helpers import err

class Member: # the base class for the classes group and task
  """The base class for the classes Task and Group.
  
    Brands the given underlying with the __ec_member__ attr, which is used to identify the Underlying as processable by ec.
  """
  def __init__(self, Underlying, Config):
    Underlying.__ec_member__ = self
    self.Underlying = Underlying
    self.Config = Config
    
class Task(Member):
  """A callable class that allows the calling of the underlying function as a task.
  """
  def __init__(self, Underlying, Args, Config):
    
    if not 'name' in Config:
      Config['name'] = Underlying.func_name
      
    Member.__init__(self, Underlying, Config)
    
    try:
      self.Args = self.__load_args__(Args)
    
    except HandledException as e:
      err(e, 1)
      
  def __call__(self, **Args):    
    self.__digest__(Args)
    try:
      return self.Underlying(**Args)
      
    except TypeError as e:
      raise HandledException(e)
  
  def __load_args__(self, Args):
    """Prepares the task for excecution.
    """
    FuncArgs = _getFuncArgs(self.Underlying)
    OrderedArgs = OrderedDict() # the order of configuration (through decorators) is prefered over the order of declaration (within the function body)
    
    for Arg in Args:
      argName = Arg.get('name')
      
      if argName is None:
        if not FuncArgs:
          raise HandledException('Excess args while configuring "%s".' % self.Config['name'])
          
        FuncArg = FuncArgs.iteritems().next() # get the first item
        argName = FuncArg[0]
        FuncArg = FuncArg[1]
        
      else:
        FuncArg = FuncArgs.get(argName)
        
        if FuncArg is None:
          raise HandledException('Unknown arg "%s" while configuring "%s".' % (argName, self.Config['name']))
          
      FuncArg.update(**Arg) # prefer Args config over the values given while defining the function.
      OrderedArgs[argName] = FuncArg
      del FuncArgs[argName]
      
    OrderedArgs.update(FuncArgs.iteritems()) # add any unconfigured args
    
    return OrderedArgs
    
  def __digest__(self, InArgs):
    """A helper for __call__ that digests the provided Args.
    """
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
        raise HandledException('Unknown arg: %s.' % k)
  
  def __collect_n_call__(self, **InArgs):
    """Helps with collecting all the args and call the Task.
    """
    self.__confirm_known_args__(InArgs)
    
    for name, Arg in self.Args.items():
      if not name in InArgs:
        InArgs[name] = self.__get_arg__(name)
        
      else:
        _type = Arg.get('type')
        try:
          InArgs[name] = _type(InArgs[name]) if _type else InArgs[name]
          
        except ValueError:
          InArgs[name] = self.__get_arg__(name)
      
    return self.Underlying(**InArgs)
    
class Group(Member):
  """Groups can contain other Members (Tasks / Groups).
  """
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
  """The base class for custom types.
  """  
  def __init__(self, desc=None):
    if desc is not None:
      self.desc = desc
  
  def __str__(self):
    return getattr(self, 'desc', '')
    
# Helper Classes
class HandledException(Exception):
  """A custom error class for ec's interanl exceptions, which are handled within ec.
  """
  
  def __init__(self, e, *args):
    self.args = args
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
from ..utils import get
