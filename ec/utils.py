r"""
utils
=====

A set of utility functions for the scripts.
"""
from modules.exposed import static
from modules.classes import CustomType
from modules import core
from modules.helpers import exit, gatherInput, reconfigArg

__all__ = ['get', 'static', 'custom', 'walk', 'exit']

def get(type=None, **ArgConfig):
  r"""Helps to interactively get user input.

  Args:
    desc (str): The description for input.
    type (type / CustomType): The type of the input (defaults to None).
  """
  ArgConfig.update(type=type)
  return gatherInput(**reconfigArg(ArgConfig))

class custom(CustomType):
  r"""Helps with creating dynamic CustomTypes on the fly.

  Args:
    validator (callable): Validates the input.
    converter (callable): Converts the input. Defaults to None.
    \*\*Config  (kwargs): The configuration of the CustomType.

  #Later: Think of merging the validator and the converter.
  """
  def __init__(self, validator=None, converter=None, **Config):
    CustomType.__init__(self, **Config)

    self.validator = validator
    self.converter = converter

  def __call__(self, val):
    if self.converter:
      val = self.converter(val)

    if self.validator and not self.validator(val):
      raise ValueError()

    return val

def walk(TargetGroup=None):
  r"""Walks the members of the given target, recursively.

  Args:
    TargetGroup (Group): The target to walk. Defaults to the BaseGroup.

  Yields:
    Member
  """
  if TargetGroup is None:
    TargetGroup = core.BaseGroup

  return _walk_worker(TargetGroup)

# Helpers
def _walk_worker(TargetGroup): # Check: Could the generator yield Member, Parent?
  for name, Member in TargetGroup.Members.items():
    if Member.Config.get('alias') == name: # don't process aliases
      continue

    yield Member

    if hasattr(Member, 'Members'): # we've got a Group
      for item in _walk_worker(Member):
        yield item
