"""
An example fro wrapping ec based modules
"""

from ec import interface

import simple # the ecd script

interface.call('task1 arg2=1', True)