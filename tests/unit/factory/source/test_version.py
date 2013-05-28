import unittest

from apidoc.factory.source.version import Version as VersionFactory

from apidoc.object.source import Version, Method, ObjectString, Type


class TestVersion(unittest.TestCase):

    def setUp(self):
        self.factory = VersionFactory()

    def test_create_from_name_and_dictionary(self):
        datas = {
            "uri": "a", "major": 1, "minor": 2, "status": "beta",
            "description": "c",
            "extends": ["v1", "v2"],
            "methods": {"m_name": {"uri": "/"}},
            "references": {"r_name": {"type": "string"}},
            "types": {"t_name": {"primary": "string"}}
        }
        response = self.factory.create_from_name_and_dictionary("o_name", datas)

        self.assertIsInstance(response, Version)
        self.assertEqual("a", response.uri)
        self.assertEqual(1, response.major)
        self.assertEqual(2, response.minor)
        self.assertIsInstance(response.status, Version.Status)
        self.assertEqual("beta", str(response.status))
        self.assertEqual("o_name", response.name)
        self.assertEqual("c", response.description)
        self.assertIn("m_name", response.methods)
        self.assertIsInstance(response.methods["m_name"], Method)
        self.assertEqual("m_name", response.methods["m_name"].name)
        self.assertIn("r_name", response.references)
        self.assertIsInstance(response.references["r_name"], ObjectString)
        self.assertEqual("r_name", response.references["r_name"].name)
        self.assertIn("t_name", response.types)
        self.assertIsInstance(response.types["t_name"], Type)
        self.assertEqual("t_name", response.types["t_name"].name)

    def test_create_from_name_and_dictionary__failed_wrong_status(self):
        with self.assertRaises(ValueError):
            self.factory.create_from_name_and_dictionary("o_name", {"status": "foo"})
