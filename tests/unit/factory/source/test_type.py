import unittest

from apidoc.factory.source.type import Type as TypeFactory

from apidoc.object.source import Type, TypeFormat, EnumType, EnumTypeValue


class TestType(unittest.TestCase):

    def setUp(self):
        self.factory = TypeFactory()

    def test_create_from_name_and_dictionary(self):
        datas = {
            "primary": "string",
            "description": "c",
            "category": "a",
            "format": {
                "pretty": "p",
                "sample": "s",
                "advanced": "d",
            }
        }
        response = self.factory.create_from_name_and_dictionary("o_name", datas)

        self.assertIsInstance(response, Type)
        self.assertEqual("o_name", response.name)
        self.assertEqual("c", response.description)
        self.assertIsInstance(response.primary, Type.Primaries)
        self.assertEqual("string", str(response.primary))
        self.assertIsInstance(response.format, TypeFormat)
        self.assertEqual("p", response.format.pretty)
        self.assertEqual("s", response.format.sample)
        self.assertEqual("d", response.format.advanced)

    def test_create_from_name_and_dictionary__failed_missing_primary(self):
        with self.assertRaises(ValueError):
            self.factory.create_from_name_and_dictionary("o_name", {})

    def test_create_from_name_and_dictionary__failed_wrong_primary(self):
        with self.assertRaises(ValueError):
            self.factory.create_from_name_and_dictionary("o_name", {"primary": "foo"})

    def test_create_from_name_and_dictionary__enum(self):
        datas = {
            "primary": "enum",
            "values": {"a": {"description": "b"}}
        }
        response = self.factory.create_from_name_and_dictionary("o_name", datas)

        self.assertIsInstance(response, EnumType)
        self.assertIsInstance(response.primary, Type.Primaries)
        self.assertEqual("enum", str(response.primary))
        self.assertIn("a", response.values)
        self.assertIsInstance(response.values["a"], EnumTypeValue)
        self.assertEqual("a", response.values["a"].name)

    def test_create_from_name_and_dictionary__enum__failed_missing_primary(self):
        with self.assertRaises(ValueError):
            self.factory.create_from_name_and_dictionary("o_name", {})

    def test_create_from_name_and_dictionary__enum__failed_wrong_primary(self):
        with self.assertRaises(ValueError):
            self.factory.create_from_name_and_dictionary("o_name", {"primary": "foo"})
