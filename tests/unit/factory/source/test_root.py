import unittest

from apidoc.factory.source.root import Root as RootFactory

from apidoc.object.source_raw import Root, Version, Configuration, Category


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

    def test_create_from_name_and_dictionary__feed_uri(self):
        datas = {"configuration": {"uri": "a"}, "versions": {"v1": {"uri": "b", "methods": {"m1": {"uri": "c"}}}}}
        response = self.factory.create_from_dictionary(datas)

        self.assertEqual("ab", response.versions["v1"].full_uri)
        self.assertEqual("abc", response.versions["v1"].methods["m1"].full_uri)
        self.assertEqual("bc", response.versions["v1"].methods["m1"].absolute_uri)
