r"""
Test ec.utils.
"""
import unittest

from ec.utils import get, static, custom, walk

from support.helpers import RawInputHook as RIH, expect_exception

# Tests
class TestUtils(unittest.TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_get(self):
    Inputs = 'a', 1
    RIH.values(*Inputs)

    # test the call
    assert(get('str') == Inputs[0])

    assert(get('int', type=int) == Inputs[1])

  def test_static(self):
    @static
    class cls: #pylint: disable=W0232
      def method(val):
        return val

    assert(cls.method(1) == 1)

  def test_custom(self):
    _type = custom(lambda v: v%2 == 1, int, type_str='an odd number')

    assert(_type(1) == 1)
    assert(expect_exception(lambda: _type(2), ValueError))
    assert(expect_exception(lambda: _type('a'), ValueError))

  def test_walk(self):
    from targets import simple
    from ec import interface

    interface.setBase(simple)

    expected = set(['task1', 'group1', 'ex', 'hex'])
    got = set()

    for Member in walk(simple.__ec_member__):
      got.add(Member.Config['name'])

    assert(expected == got)

if __name__ == '__main__':
  unittest.main()
