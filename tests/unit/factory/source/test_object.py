import unittest

from apidoc.factory.source.object import Object as ObjectFactory

from apidoc.object.source_raw import Object, ObjectObject, ObjectArray
from apidoc.object.source_raw import ObjectNumber, ObjectString, ObjectBool, ObjectNone
from apidoc.object.source_raw import ObjectDynamic, ObjectReference, ObjectType, ObjectConst


class TestObject(unittest.TestCase):

    def setUp(self):
        self.factory = ObjectFactory()

    def test_create_from_name_and_dictionary(self):
        datas = {
            "description": "c",
            "type": "object",
            "properties": {
                "foo": {
                    "type": "string",
                    "description": "c_foo",
                    "optional": "true",
                    "required": "true",
                    "sample": "s_foo"
                },
                "bar": {
                    "type": "number",
                    "description": "c_bar",
                    "optional": "false",
                    "required": "false",
                    "sample": "123.4"
                },
                "baz": {
                    "type": "bool",
                    "description": "c_baz",
                    "sample": "true"
                },
                "qux": {
                    "type": "none",
                    "description": "c_qux"
                },
                "fum": {
                    "type": "reference",
                    "description": "c_fum",
                    "reference": "r_fum"
                },
                "foofoo": {
                    "type": "dynamic",
                    "description": "c_foofoo",
                    "items": "t_foofoo",
                    "sample": {
                        "a": "b",
                        "c": "d"
                    }
                },
                "foobar": {
                    "type": "t_foobar",
                    "description": "c_foobar",
                    "sample": "s_foobar"
                },
                "foobaz": {
                    "type": "array",
                    "description": "c_foobaz",
                    "sample_count": 2,
                    "items": {
                        "type": "object",
                        "properties": {
                            "fooqux": {
                                "type": "string"
                            }
                        }
                    }
                },
                "fooqux": {
                    "type": "const",
                    "description": "c_fooqux",
                    "const_type": "number",
                    "value": "d_fooqux"
                }
            }
        }

        response = self.factory.create_from_name_and_dictionary("o_name", datas)

        self.assertIsInstance(response, ObjectObject)
        self.assertIsInstance(response.type, Object.Types)
        self.assertEqual("object", str(response.type))
        self.assertEqual("c", response.description)

        self.assertIn("foo", response.properties)
        self.assertIsInstance(response.properties["foo"], ObjectString)
        self.assertEqual("c_foo", response.properties["foo"].description)
        self.assertEqual("foo", response.properties["foo"].name)
        self.assertEqual("s_foo", response.properties["foo"].sample)
        self.assertEqual(True, response.properties["foo"].optional)
        self.assertEqual(True, response.properties["foo"].required)

        self.assertIn("bar", response.properties)
        self.assertIsInstance(response.properties["bar"], ObjectNumber)
        self.assertEqual("c_bar", response.properties["bar"].description)
        self.assertEqual("bar", response.properties["bar"].name)
        self.assertEqual("123.4", response.properties["bar"].sample)
        self.assertEqual(False, response.properties["bar"].optional)
        self.assertEqual(False, response.properties["bar"].required)

        self.assertIn("baz", response.properties)
        self.assertIsInstance(response.properties["baz"], ObjectBool)
        self.assertEqual("c_baz", response.properties["baz"].description)
        self.assertEqual("baz", response.properties["baz"].name)
        self.assertEqual(True, response.properties["baz"].sample)
        self.assertEqual(False, response.properties["baz"].optional)
        self.assertEqual(True, response.properties["baz"].required)

        self.assertIn("qux", response.properties)
        self.assertIsInstance(response.properties["qux"], ObjectNone)
        self.assertEqual("c_qux", response.properties["qux"].description)
        self.assertEqual("qux", response.properties["qux"].name)

        self.assertIn("fum", response.properties)
        self.assertIsInstance(response.properties["fum"], ObjectReference)
        self.assertEqual("c_fum", response.properties["fum"].description)
        self.assertEqual("fum", response.properties["fum"].name)
        self.assertEqual("r_fum", response.properties["fum"].reference_name)

        self.assertIn("foofoo", response.properties)
        self.assertIsInstance(response.properties["foofoo"], ObjectDynamic)
        self.assertEqual("c_foofoo", response.properties["foofoo"].description)
        self.assertEqual("foofoo", response.properties["foofoo"].name)
        self.assertEqual("t_foofoo", response.properties["foofoo"].items)
        self.assertEqual({"a": "b", "c": "d"}, response.properties["foofoo"].sample)

        self.assertIn("foobar", response.properties)
        self.assertIsInstance(response.properties["foobar"], ObjectType)
        self.assertEqual("c_foobar", response.properties["foobar"].description)
        self.assertEqual("foobar", response.properties["foobar"].name)
        self.assertEqual("t_foobar", response.properties["foobar"].type_name)
        self.assertEqual("s_foobar", response.properties["foobar"].sample)

        self.assertIn("foobaz", response.properties)
        self.assertIsInstance(response.properties["foobaz"], ObjectArray)
        self.assertEqual("c_foobaz", response.properties["foobaz"].description)
        self.assertEqual("foobaz", response.properties["foobaz"].name)
        self.assertEqual(2, response.properties["foobaz"].sample_count)
        self.assertIsInstance(response.properties["foobaz"].items, ObjectObject)
        self.assertEqual("items", response.properties["foobaz"].items.name)

        self.assertIn("fooqux", response.properties)
        self.assertIsInstance(response.properties["fooqux"], ObjectConst)
        self.assertEqual("c_fooqux", response.properties["fooqux"].description)
        self.assertEqual("fooqux", response.properties["fooqux"].name)
        self.assertEqual("number", response.properties["fooqux"].const_type)
        self.assertEqual("d_fooqux", response.properties["fooqux"].value)

    def test_create_from_name_and_dictionary__failed_missing_type(self):
        with self.assertRaises(ValueError):
            self.factory.create_from_name_and_dictionary("o_name", {})

    def test_create_from_name_and_dictionary__failed_wrong_type(self):
        with self.assertRaises(ValueError):
            self.factory.create_from_name_and_dictionary("o_name", {"type": "dynamic", "sample": []})

    def test_create_from_name_and_dictionary__failed_wrong_const_type(self):
        with self.assertRaises(ValueError):
            self.factory.create_from_name_and_dictionary("o_name", {"type": "const", "const_type": "baz"})

    def test_create_from_name_and_dictionary__failed_missing_value(self):
        with self.assertRaises(ValueError):
            self.factory.create_from_name_and_dictionary("o_name", {"type": "const", "const_type": "string"})

    def test_create_from_name_and_dictionary__default_const_type(self):
        response = self.factory.create_from_name_and_dictionary("o_name", {"type": "const", "value": "abc"})
        self.assertEqual(ObjectConst.Types.string, response.const_type)
