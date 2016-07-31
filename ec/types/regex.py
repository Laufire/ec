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
_hostPattern = r'([\da-z\.-]+)\.([a-z\.]{2,6})'

# Quick Templates
email = pattern(r'^([a-z0-9_\.-]+)@%s$' % _hostPattern, type_str='Email')
username = pattern(r'^[a-z0-9_-]{3,16}$', type_str='Username')
password = pattern(r'^.+$', type_str='Password, a non-empty, spaceless string')
safe_password = pattern(r'^[A-z0-9_-]{6,18}$', type_str='Password')
slug = pattern(r'^[a-z0-9-]+$', type_str='Slug')
number = pattern(r'^[0-9]+$', type_str='Number') # a positive integer
host = pattern(r'^%s$' % _hostPattern, type_str='Host')
route = pattern(r'^(\/[A-z0-9_-]+)*$', type_str='route')
