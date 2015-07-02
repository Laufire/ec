#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests the dispatch mode.
"""

import unittest

from support.helpers import shell_exec

def dispatch(argStr):
  return shell_exec('python support/target_script.py %s' % argStr)
  
class TestPrivate(unittest.TestCase):

  def setUp(self):
    pass

  def tearDown(self):
    pass
    
  def test_dispatch(self):
    Result = dispatch('task1 arg1=1')
    
    assert(Result['code'] == 0)
    assert(Result['out'].strip() == '1 2')
    
  def test_multiple_args(self):
    Result = dispatch('task1 arg1=1 arg2=1')
    
    assert(Result['code'] == 0)
    assert(Result['out'].strip() == '1 1')
    
  def test_flag_help(self):
    Result = dispatch('-h')
    
    assert(Result['code'] == 0)
    assert(Result['out'].strip()[:5] == 'Usage')
    
  def test_no_task(self):
    Result = dispatch('task2')
    
    assert(Result['code'] == 1)
    assert(Result['err'].strip()[:2] == 'No')
    
  def test_nested_task(self):
    Result = dispatch('group1 task1 arg1=1')
    
    assert(Result['code'] == 0)
    assert(Result['out'].strip() == '1')

  def test_default_arg(self):
    Result = dispatch('task1 arg1=1')
    
    assert(Result['code'] == 0)
    assert(Result['out'].strip() == '1 2')
  
if __name__ == '__main__':
  unittest.main()
