import unittest

from apidoc.lib.util.enum import Enum


class TestEnum(unittest.TestCase):

    def test_contains_int(self):
        self.assertTrue(1 in Foo)
        self.assertFalse(3 in Foo)

    def test_contains_name(self):
        self.assertTrue("bar" in Foo)
        self.assertFalse("qux" in Foo)

    def test_contains_other(self):
        self.assertFalse(object() in Foo)

    def test_instance(self):
        self.assertEqual(Foo(1), Foo.bar)
        self.assertEqual(Foo("bar"), Foo.bar)

    def test_repr(self):
        self.assertEqual("Foo.bar", repr(Foo(1)))

    def test_new__boolean(self):
        self.assertEqual(None, Foo(object))


class Foo(Enum):
    bar = 1
    baz = 2
