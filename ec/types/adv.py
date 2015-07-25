"""
adv
===
Advanced types.
"""
import shlex

from ..modules.classes import CustomType, HandledException
from ..modules.helpers import getDigestableArgs

class t2t(CustomType):
  """Convert a ec task into a type.
  
  Args:
    __ec__task__: Any ec task.
  """
  def __init__(self, __ec__task__, **Defaults):
    __ec_member__ = __ec__task__.__ec_member__
    Config = __ec_member__.Config
    
    CustomType.__init__(self, desc=Config['desc'] if 'desc' in Config else None)
    
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
    desc (str): The description for the chain.
    
  Example:
  
    @arg(type=chain(exists, isabs), desc="an existing abs path")
  """
  def __init__(self, *Types, **Kwargs):
    CustomType.__init__(self, Kwargs.get('desc'))
    
    self.Types = Types
    self.CurrentType = None
    
  def __call__(self, val):
    
    for Type in self.Types:
      self.CurrentType = Type
      val = Type(val)
    
    return val
    
  def __str__(self):
    return getattr(self, 'desc', str(self.CurrentType) if self.CurrentType else '')
    
class invert(CustomType):
  """Inverts the given type.
  
  ie: Only failed values are qualified.
  
  Args:
    desc (str): The description for the type.
    
  Example:
  
    @arg(type=invert(exists), desc="a free path")
  """
  def __init__(self, Type, desc=None):
    CustomType.__init__(self, desc)
    
    self.Type = Type
    
  def __call__(self, val):
    
    try:
      self.Type(val)
      
    except (ValueError, TypeError):
      return val
    
    raise ValueError()
    
  def __str__(self):
    return getattr(self, 'desc', 'a value that is not %s' % str(self.Type))
