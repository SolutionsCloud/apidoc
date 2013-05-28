import unittest

from apidoc.factory.source.configuration import Configuration as ConfigurationFactory

from apidoc.object.source import Configuration


class TestConfiguration(unittest.TestCase):

    def setUp(self):
        self.factory = ConfigurationFactory()

    def test_create_from_dictionary(self):
        datas = {"title": "foo", "description": "bar", "uri": "baz"}
        response = self.factory.create_from_dictionary(datas)

        self.assertIsInstance(response, Configuration)
        self.assertEqual("foo", response.title)
        self.assertEqual("bar", response.description)
        self.assertEqual("baz", response.uri)
