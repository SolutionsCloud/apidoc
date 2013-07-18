import unittest

from apidoc.lib.util.serialize import json_repr
from apidoc.lib.util.enum import Enum


class TestSerialize(unittest.TestCase):

    def test_json_repr__None(self):
        self.assertEqual('null', json_repr(None))

    def test_json_repr__Number(self):
        self.assertEqual('1.2', json_repr(1.2))

    def test_json_repr__String(self):
        self.assertEqual('"foo\\"bar"', json_repr('foo"bar'))

    def test_json_repr__Dict(self):
        self.assertIn('"a": 1', json_repr({"b": 2, "a": 1}))
        self.assertIn('"b": 2', json_repr({"b": 2, "a": 1}))

    def test_json_repr__List(self):
        self.assertEqual('[1, 2]', json_repr([1, 2]))

    def test_json_repr__Tupple(self):
        self.assertEqual('[1, 2]', json_repr((1, 2)))

    def test_json_repr__ObjectDiff(self):
        self.assertIn('"b": 1', json_repr(objectDict()))
        self.assertIn('"c": 2', json_repr(objectDict()))

    def test_json_repr__ObjectEnum(self):
        self.assertEqual('"a"', json_repr(objectEnum.a))

    def test_json_repr__ObjectOher(self):
        self.assertIn('proxy(', json_repr(type("")))


class objectDict():

    def __init__(self):
        self.b = 1
        self.c = 2


class objectOther():

    def __init__(self):
        pass


class objectEnum(Enum):

    """List of availables Status for this element
    """
    a = 1
    b = 2
