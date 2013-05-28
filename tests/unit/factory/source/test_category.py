import unittest

from apidoc.factory.source.category import Category as CategoryFactory

from apidoc.object.source import Category


class TestCategory(unittest.TestCase):

    def setUp(self):
        self.factory = CategoryFactory()

    def test_create_from_name_and_dictionary(self):
        datas = {
            "description": "c",
            "order": "10"
        }
        response = self.factory.create_from_name_and_dictionary("o_name", datas)

        self.assertIsInstance(response, Category)
        self.assertEqual("o_name", response.name)
        self.assertEqual("c", response.description)
