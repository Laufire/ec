import shlex

from ..modules.classes import CustomType
from ..modules.helpers import list2dict

class t2t(CustomType):
  """
  Converts a ec task into a type.
  """
  def __init__(self, __pr__task__, **InArgs):
    __pr_member__ = __pr__task__.__pr_member__
    Config = __pr_member__.Config
    
    CustomType.__init__(self, desc=Config['desc'] if 'desc' in Config else None)
    
    self.Task = __pr_member__
    self.InArgs = InArgs
  
  def __call__(self, val):
    Args = self.InArgs.copy()
    Args.update(**list2dict(shlex.split(val)))
    
    return self.Task.__collect_n_call__(**Args)
    