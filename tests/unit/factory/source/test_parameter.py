import unittest

from apidoc.factory.source.parameter import Parameter as ParameterFactory

from apidoc.object.source_raw import Parameter


class TestParameter(unittest.TestCase):

    def setUp(self):
        self.factory = ParameterFactory()

    def test_create_from_name_and_dictionary(self):
        datas = {
            "description": "c",
            "type": "a",
            "sample": "b",
            "optional": "1"
        }
        response = self.factory.create_from_name_and_dictionary("o_name", datas)

        self.assertIsInstance(response, Parameter)
        self.assertEqual("o_name", response.name)
        self.assertEqual("c", response.description)
        self.assertEqual("a", response.type)
        self.assertEqual("b", response.sample)
        self.assertEqual(True, response.optional)
