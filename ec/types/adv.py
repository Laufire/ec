import shlex

from ..modules.classes import CustomType, HandledException
from ..modules.helpers import list2dict

class t2t(CustomType):
  """Convert a ec task into a type.
  """
  def __init__(self, __ec__task__, **InArgs):
    __ec_member__ = __ec__task__.__ec_member__
    Config = __ec_member__.Config
    
    CustomType.__init__(self, desc=Config['desc'] if 'desc' in Config else None)
    
    self.Task = __ec_member__
    self.InArgs = InArgs
  
  def __call__(self, val):
    Args = self.InArgs.copy()
    Args.update(**list2dict(shlex.split(val)))
    
    return self.Task.__collect_n_call__(**Args)
    
class chain(CustomType):
  def __init__(self, *Types, **Kwargs):
    """Combines mutiple types into one.
    
    Args:
      *Types (Type): The types to chain.
      
    Kwargs:
      desc (str): The description for the chain.
      
    Example:
    
      @arg(type=chain(exists, isabs), desc="an existing abs path")
    """
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
