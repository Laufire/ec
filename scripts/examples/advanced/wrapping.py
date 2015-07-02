"""
An example for wrapping ec based modules.
"""

from ec import interface

import simple # the ec-ed script

interface.call('task1 arg2=1', True)