r"""
regex
=====
Types based on regular expressions.
"""

import re

from ..modules.classes import CustomType

class pattern(CustomType):
  r"""Get inputs that fit a specific pattern.
  """
  def __init__(self, pattern, flags=0, **Config):
    self.exp = re.compile(pattern, flags)

    if not 'type_str' in Config:
      Config['type_str'] = 'a string matching the pattern \'%s\'' % self.exp.pattern

    CustomType.__init__(self, **Config)

  def __call__(self, val):
    if not self.exp.match(val):
      raise ValueError()

    return val

# Data
_host_pattern = r'([\da-z\.-]+)\.([a-z\.]{2,6})'

_safe_string_pattern = r'^[a-z0-9_]{3,16}$'

# Quick Templates
email = pattern(r'^([a-z0-9_\.-]+)@%s$' % _host_pattern, type_str='email')

hex = pattern(r'^[a-fA-F0-9-]+$', type_str='hex')

host = pattern(r'^%s$' % _host_pattern, type_str='host')

number = pattern(r'^[0-9]+$', type_str='number') # a positive integer

password = pattern(r'^.+$', type_str='password, a non-empty, spaceless string')

route = pattern(r'^(\/[A-z0-9_-]+)*$', type_str='route')

safe_string = pattern(_safe_string_pattern, type_str='safe_string')

safe_password = pattern(r'^[A-z0-9_-]{6,18}$', type_str='password')

safe_path = pattern(r'^\/*([A-z0-9_-]+\/*)*$', type_str='safe path')

slug = pattern(r'^[a-z0-9-]+$', type_str='slug')

username = pattern(_safe_string_pattern, type_str='username')
