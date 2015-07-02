"""
An example fro wrapping private based modules
"""

from private import interface

import simple # the privated script

interface.call('task1 arg2=1', True)