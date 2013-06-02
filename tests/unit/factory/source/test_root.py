import unittest

from apidoc.factory.source.root import RootFactory as RootFactory

from apidoc.object.source import Root, Version, Configuration, Category


class TestRoot(unittest.TestCase):

    def setUp(self):
        self.factory = RootFactory()

    def test_create_from_name_and_dictionary(self):
        datas = {"versions": {"v1": {}, "v2": {}}, "configuration": {"title": "foo"}, "categories": {"c1": {}}}
        response = self.factory.create_from_dictionary(datas)

        self.assertIsInstance(response, Root)
        self.assertEqual(2, len(response.versions))
        self.assertIn("v1", response.versions)
        self.assertIsInstance(response.versions["v1"], Version)
        self.assertIn("v2", response.versions)
        self.assertEqual("v2", response.versions["v2"].name)
        self.assertIsInstance(response.configuration, Configuration)
        self.assertEqual("foo", response.configuration.title)
        self.assertEqual(1, len(response.categories))
        self.assertIn("c1", response.categories)
        self.assertIsInstance(response.categories["c1"], Category)
