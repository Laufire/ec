r"""
All the classes of ec.
"""
from collections import OrderedDict

class Member():
  r"""The base class for the classes Task and Group.

    It brands the given underlying with the __ec_member__ attr, which is used to identify the Underlying as processable by ec.
  """
  def __init__(self, Underlying, Config):
    __ec_member__ = getattr(Underlying, '__ec_member__', None)
    if 'name' in Config:
      validateName(Config['name'])

    else:
      Config['name'] = getattr(Underlying, 'func_name', Underlying.__name__).rsplit('.', 1)[-1]

    if __ec_member__:
      __ec_member__.Config.update(Config)
      self.Config = __ec_member__.Config

    else:
      Underlying.__ec_member__ = self
      self.Config = Config

    self.Underlying = Underlying

class Task(Member):
  r"""A callable class that allows the calling of the underlying function as a task.
  """
  def __init__(self, Underlying, Args, Config):
    Member.__init__(self, Underlying, Config)

    self.Args = self.__load_args__(Args)

  def __load_args__(self, Args):
    r"""Prepares the task for excecution.
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
        validateName(argName)

        FuncArg = FuncArgs.get(argName)

        if FuncArg is None:
          raise HandledException('Unknown arg "%s" while configuring "%s".' % (argName, self.Config['name']))

      FuncArg['name'] = argName
      FuncArg.update(Arg) # prefer Args config over the values given while defining the function.

      OrderedArgs[argName] = reconfigArg(FuncArg)
      del FuncArgs[argName]

    for name, Config in FuncArgs.iteritems(): # process the unconfigured arguments
      Config['name'] = name
      OrderedArgs[name] = reconfigArg(Config)

    return OrderedArgs

  def __confirm_known_args__(self, InArgs):
    r"""Confirms that only known args are passed to the underlying.
    """
    ArgKeys = self.Args.keys()

    for k in InArgs.keys():
      if k not in ArgKeys:
        raise HandledException('Unknown arg: %s.' % k, Member=self)

  def __digest_args__(self, InArgs, InKwArgs):
    r"""Digests the given Args and KwArgs and returns a KwArgs dictionary.
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
          KwArgs[name] = default

        else:
          raise HandledException('Missing argument: %s.' % name, Member=self)

      else:
        if _type:
          try:
            KwArgs[name] = _type(KwArgs[name])

          except (ValueError, TypeError):
            raise HandledException('Invalid value for "%s", expected %s; got "%s".' % (name, _type, KwArgs[name]), help_type='task', Member=self)

    return self.Underlying(**KwArgs)

  def __collect_n_call__(self, *InArgs, **InKwArgs):
    r"""Helps with collecting all the args and call the Task.
    """
    KwArgs = self.__digest_args__(InArgs, InKwArgs)

    for name, Arg in self.Args.items():
      if not name in KwArgs:
        KwArgs[name] = gatherInput(**Arg)

      else:
        _type = Arg.get('type')
        try:
          KwArgs[name] = _type(KwArgs[name]) if _type else KwArgs[name]

        except (ValueError, TypeError):
          KwArgs[name] = gatherInput(**Arg)

    return self.Underlying(**KwArgs)

class Group(Member):
  r"""Groups can contain other Members (Tasks / Groups).

  Note:
    Groups that have modules as their underlying would have it's members loaded by ec.start.
  """
  def __init__(self, Underlying, Config):
    Member.__init__(self, Underlying, Config or {})

class CustomType:
  r"""The base class for custom types.

  Args:
    **Config (kwargs): Configuration for the custom type.

  Config:
    type_str (str, optional): The string representation of the type.

  Note:
    Config supports the same keywords as config.arg, with some additions to it. While inheriting the class, these keywords shouldn't be used as variable names.
  """
  def __init__(self, **Config):
    self._Config = Config
    self.str = Config['type_str'] if 'type_str' in Config else 'custom type'

  def __str__(self):
    r"""Used to represent the type as a string, in messages and queries.
    """
    return getattr(self, 'str', 'custom type')

  def __ec_config__(self, ArgConfig):
    r"""Used to reconfigure arg configurations.

    Args:
      ArgConfig (dict): The configuration to be modified.

    Returns:
      ArgConfig (dict): The modified configuration.

    Notes:

      * This method allows CustomTypes to modify the configuration of the calling arg.
      * This is the signature method used for duck typing CustomType.
      * With custom implementations the method should set the key 'type_str', as well as return the modified ArgConfig.
    """
    type_str = self.str

    if 'default' in ArgConfig:
      type_str += ' (%s)' % ArgConfig['default']

    ArgConfig['type_str'] = type_str

    return ArgConfig

# Helper Classes
class HandledException(Exception):
  r"""A custom error class for ec's internal exceptions, which are handled within ec.
  """

  def __init__(self, e, **Info):
    self.Info = Info
    super(HandledException, self).__init__(getattr(e, 'message', e))

# Helpers
def _getFuncArgs(func):
  r"""Gives the details on the args of the given func.

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
from helpers import validateName, gatherInput, reconfigArg
