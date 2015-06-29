from collections import OrderedDict

from helpers import err

class Member: # the base class for the classes group and task
  def __init__(self, doc):
    self.Config = {}
    self.__doc__ = doc # allow the docstrigs to be used by external modules
    
class Task(Member):
  def __init__(self, Underlying):
    Member.__init__(self, Underlying.__doc__)
    
    self.Underlying = Underlying
    self.Args = []
    
  def __call__(self, **Args):    
    self.__digest__(Args)
    try:
      return self.Underlying(**Args)
      
    except TypeError as e:
      raise HandledException(e)
  
  def __prepare__(self): # prepares the task for excecution
    FuncArgs = getFuncArgs(self.Underlying)
    TaskArgs = self.Args
    OrderedArgs = OrderedDict() # the order of configuration (through decorators) is prefered over the order of declaration (within the function body)
    
    # import pdb; pdb.set_trace()
    for k, Arg in TaskArgs:
      FuncArg = FuncArgs.get(k)
      if FuncArg:
        FuncArg.update(**Arg) # prefer Args config over the values given while defining the function.
        Arg = FuncArg
        
      del FuncArgs[k]
      OrderedArgs[k] = Arg
      
    OrderedArgs.update(**FuncArgs)
    self.Args = OrderedArgs
    
  def __digest__(self, InArgs): # should be called only from __call__
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
            raise HandledException('Invalid value for "%s", expected a value of "%s", got "%s".' % (name, _type, InArgs[name]))
      
  def __collect_arg__(self, argName): # collect a single arg
    Arg = self.Args[argName]
    _type = Arg.get('type')
    has_default = 'default' in Arg
    Default = Arg.get('default')
    
    while True:
      try:
        line = raw_input('%s%s: ' % (argName, ' (%s) ' % Default if has_default else ''))
        
        if not line:
          if has_default:
            return Arg['default']
          
        return _type(line) if _type else line
        
      except ValueError:
        Parts = []
        if 'desc' in Arg: Parts.append(Arg['desc'])
        if _type: Parts.append(str(_type))
        
        err(' '.join(Parts) if Parts else '<invalid value>')
    
  def collectNcall(self, **InArgs): # collect all the args and call the Task
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
  def __init__(self, Underlying):
    Member.__init__(self, Underlying.__doc__)
    
    self.Underlying = Underlying
    self.Config['Members'] = Members = getattr(Underlying, '__config__', {})
    
    for Item in vars(Underlying).values(): # collect all the children
      if isinstance(Item, Member):
        Members[Item.Config.get('name', getattr(Item.Underlying, 'func_name' if isinstance(Item, Task) else '__name__'))] = Item
    
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
  