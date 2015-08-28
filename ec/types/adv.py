"""
adv
===
Advanced types.
"""
import shlex

from ..modules.classes import CustomType, HandledException
from ..modules.helpers import getDigestableArgs, getTypeStr

class t2t(CustomType):
  """Convert a ec task into a type.

  Args:
    __ec__task__: Any ec task.
  """
  def __init__(self, __ec__task__, **Defaults):
    __ec_member__ = __ec__task__.__ec_member__
    Config = __ec_member__.Config

    CustomType.__init__(self, type_str=Config['desc'])

    self.Task = __ec_member__
    self.Defaults = Defaults

  def __call__(self, val):
    KwArgs = self.Defaults.copy()
    DigestableArgs = getDigestableArgs(shlex.split(val))
    KwArgs.update(**DigestableArgs[1])

    return self.Task.__collect_n_call__(*DigestableArgs[0], **KwArgs)

class chain(CustomType):
  """Combines mutiple types into one.

  Args:
    *Types (Type): The types to chain.

  Kwargs:
    type_str (str): The description for the chain.

  Example:

    @arg(type=chain(exists, isabs), type_str="an existing abs path")
  """
  def __init__(self, *Types, **Kwargs):
    CustomType.__init__(self, type_str=Kwargs.get('type_str', 'a chain of types (%s)' % ', '.join([getTypeStr(_type) for _type in Types])))

    self.Types = Types
    self.CurrentType = None

  def __call__(self, val):

    for Type in self.Types:
      self.CurrentType = Type
      val = Type(val)

    return val

  def __str__(self):
    return getattr(self, 'type_str', str(self.CurrentType) if self.CurrentType else '')

class invert(CustomType):
  """Inverts the given type.

  ie: Only failed values are qualified.

  Args:
    type_str (str): The description for the type.

  Example:

    @arg(type=invert(exists), type_str="a free path")
  """
  def __init__(self, Type, type_str=None):
    CustomType.__init__(self, type_str=type_str or 'anything but of type %s' % getTypeStr(Type))

    self.Type = Type

  def __call__(self, val):

    try:
      self.Type(val)

    except (ValueError, TypeError):
      return val

    raise ValueError()
