import unittest

from apidoc.factory.source.type import Type as TypeFactory

from apidoc.object.source_raw import Type, TypeFormat, ObjectString


class TestType(unittest.TestCase):

    def setUp(self):
        self.factory = TypeFactory()

    def test_create_from_name_and_dictionary(self):
        datas = {
            "description": "c",
            "category": "a",
            "item": {
                "type": "string"
            },
            "format": {
                "pretty": "p",
                "advanced": "d",
            }
        }
        response = self.factory.create_from_name_and_dictionary("o_name", datas)

        self.assertIsInstance(response, Type)
        self.assertEqual("o_name", response.name)
        self.assertEqual("c", response.description)
        self.assertIsInstance(response.item, ObjectString)
        self.assertIsInstance(response.format, TypeFormat)
        self.assertEqual("p", response.format.pretty)
        self.assertEqual("d", response.format.advanced)

    def test_create_from_name_and_dictionary__without_format(self):
        datas = {
            "description": "c",
            "category": "a",
            "item": {
                "type": "string"
            }
        }
        response = self.factory.create_from_name_and_dictionary("o_name", datas)

        self.assertIsInstance(response, Type)
        self.assertIsInstance(response.format, TypeFormat)
        self.assertEqual(None, response.format.pretty)
        self.assertEqual(None, response.format.advanced)

    def test_create_from_name_and_dictionary__without_formats_datas(self):
        datas = {
            "description": "c",
            "category": "a",
            "item": {
                "type": "string"
            },
            "format": {
            }
        }
        response = self.factory.create_from_name_and_dictionary("o_name", datas)

        self.assertIsInstance(response, Type)
        self.assertIsInstance(response.format, TypeFormat)
        self.assertEqual(None, response.format.pretty)
        self.assertEqual(None, response.format.advanced)

    def test_create_from_name_and_dictionary__failed_missing_item(self):
        with self.assertRaises(ValueError):
            self.factory.create_from_name_and_dictionary("o_name", {})
