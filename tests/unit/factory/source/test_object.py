import unittest

from apidoc.factory.source.object import Object as ObjectFactory

from apidoc.object.source_raw import Object, ObjectObject, ObjectArray, Constraint
from apidoc.object.source_raw import ObjectNumber, ObjectInteger, ObjectString, ObjectBoolean, ObjectNone, ObjectEnum
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
                    "sample": "s_foo"
                },
                "bar": {
                    "type": "number",
                    "description": "c_bar",
                    "optional": "false",
                    "sample": "123.4"
                },
                "barfoo": {
                    "type": "integer",
                    "description": "c_barfoo",
                    "optional": "false",
                    "sample": "123"
                },
                "baz": {
                    "type": "boolean",
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
                    "items": {
                        "type": "object",
                        "properties": {
                            "fooqux": {
                                "type": "string"
                            }
                        }
                    },
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
                },
                "foofum": {
                    "type": "enum",
                    "description": "c_foofum",
                    "values": [
                        "a_foofum",
                        "b_foofum",
                    ],
                    "descriptions": {
                        "a_foofum": "d_foofum"
                    }

                },
                "barbar": {
                    "description": "c_barbar",
                }
            },
            "patternProperties": {
                "farfoo": {
                    "type": "string"
                }
            },
            "additionalProperties": {
                "type": "string"
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

        self.assertIn("bar", response.properties)
        self.assertIsInstance(response.properties["bar"], ObjectNumber)
        self.assertEqual("c_bar", response.properties["bar"].description)
        self.assertEqual("bar", response.properties["bar"].name)
        self.assertEqual("123.4", response.properties["bar"].sample)
        self.assertEqual(False, response.properties["bar"].optional)

        self.assertIn("barfoo", response.properties)
        self.assertIsInstance(response.properties["barfoo"], ObjectInteger)
        self.assertEqual("c_barfoo", response.properties["barfoo"].description)
        self.assertEqual("barfoo", response.properties["barfoo"].name)
        self.assertEqual("123", response.properties["barfoo"].sample)
        self.assertEqual(False, response.properties["barfoo"].optional)

        self.assertIn("baz", response.properties)
        self.assertIsInstance(response.properties["baz"], ObjectBoolean)
        self.assertEqual("c_baz", response.properties["baz"].description)
        self.assertEqual("baz", response.properties["baz"].name)
        self.assertEqual(True, response.properties["baz"].sample)
        self.assertEqual(False, response.properties["baz"].optional)

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
        self.assertIsInstance(response.properties["foofoo"].items, ObjectObject)
        self.assertEqual("items", response.properties["foofoo"].items.name)
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

        self.assertIn("foofum", response.properties)
        self.assertIsInstance(response.properties["foofum"], ObjectEnum)
        self.assertEqual("c_foofum", response.properties["foofum"].description)
        self.assertEqual("foofum", response.properties["foofum"].name)
        self.assertEqual(["a_foofum", "b_foofum"], response.properties["foofum"].values)
        self.assertEqual(2, len(response.properties["foofum"].descriptions))

        self.assertIn("barbar", response.properties)
        self.assertIsInstance(response.properties["barbar"], Object)
        self.assertEqual("c_barbar", response.properties["barbar"].description)
        self.assertEqual("barbar", response.properties["barbar"].name)

        self.assertIn("farfoo", response.pattern_properties)
        self.assertIsInstance(response.pattern_properties["farfoo"], ObjectString)
        self.assertIsInstance(response.additional_properties, ObjectString)

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

    def test_create_from_name_and_dictionary__array_default(self):
        datas = {
            "type": "array",
        }

        response = self.factory.create_from_name_and_dictionary("o_name", datas)

        self.assertIsInstance(response, ObjectArray)
        self.assertEqual(None, response.items)
        self.assertEqual(2, response.sample_count)

    def test_create_from_name_and_dictionary__boolean_default(self):
        datas = {
            "type": "boolean",
        }

        response = self.factory.create_from_name_and_dictionary("o_name", datas)

        self.assertIsInstance(response, ObjectBoolean)
        self.assertEqual(None, response.sample)

    def test_create_from_name_and_dictionary__reference_default(self):
        datas = {
            "type": "reference",
        }

        response = self.factory.create_from_name_and_dictionary("o_name", datas)

        self.assertIsInstance(response, ObjectReference)
        self.assertEqual(None, response.reference_name)

    def test_create_from_name_and_dictionary__dynamic_default(self):
        datas = {
            "type": "dynamic",
        }

        response = self.factory.create_from_name_and_dictionary("o_name", datas)

        self.assertIsInstance(response, ObjectDynamic)
        self.assertEqual(None, response.sample)

    def test_create_from_name_and_dictionary__new_type(self):
        ObjectObject.Types.foo = "foo"
        datas = {
            "type": "foo",
        }

        response = self.factory.create_from_name_and_dictionary("o_name", datas)

        del ObjectObject.Types.foo
        self.assertIsInstance(response, Object)

    def test_create_from_name_and_dictionary__enum_without_value(self):
        with self.assertRaises(ValueError):
            self.factory.create_from_name_and_dictionary("o_name", {"type": "enum"})

    def test_create_from_name_and_dictionary__enum_without_descriptions(self):
        response = self.factory.create_from_name_and_dictionary("o_name", {"type": "enum", "values": ["a"]})
        self.assertEqual(1, len(response.descriptions))
        self.assertEqual("a", response.descriptions[0].name)
        self.assertEqual(None, response.descriptions[0].description)

    def test_create_from_name_and_dictionary__additional_properties_false(self):
        response = self.factory.create_from_name_and_dictionary("o_name", {"type": "object", "additionalProperties": False})
        self.assertEqual(None, response.additional_properties)

    def test_create_from_name_and_dictionary__additional_properties_true(self):
        with self.assertRaises(ValueError):
            self.factory.create_from_name_and_dictionary("o_name", {"type": "object", "additionalProperties": True})

    def test_create_from_name_and_dictionary__constraint(self):
        datas = {
            "description": "c",
            "type": "object",
            "properties": {
                "foo": {
                    "type": "string",
                    "maxLength": 32,
                    "constraints": {
                        "custom": "bar"
                    }
                }
            }
        }

        response = self.factory.create_from_name_and_dictionary("o_name", datas)

        self.assertIn("foo", response.properties)
        self.assertIsInstance(response.properties["foo"], ObjectString)
        self.assertIsInstance(response.properties["foo"].constraints, dict)
        self.assertIn("maxLength", response.properties["foo"].constraints)
        self.assertIn("custom", response.properties["foo"].constraints)
        self.assertIsInstance(response.properties["foo"].constraints["maxLength"], Constraint)
        self.assertEqual("maxLength", response.properties["foo"].constraints["maxLength"].name)
        self.assertEqual(32, response.properties["foo"].constraints["maxLength"].constraint)

        self.assertTrue(response.properties["foo"].constraints["maxLength"] > response.properties["foo"].constraints["custom"])
