import unittest

from apidoc.factory.source.responseCode import ResponseCode as ResponseCodeFactory

from apidoc.object.source_raw import ResponseCode


class TestResponseCode(unittest.TestCase):

    def setUp(self):
        self.factory = ResponseCodeFactory()

    def test_create_from_dictionary(self):
        datas = {
            "code": 200,
            "description": "c",
            "message": "a",
        }
        response = self.factory.create_from_dictionary(datas)

        self.assertIsInstance(response, ResponseCode)
        self.assertEqual("200", response.name)
        self.assertEqual("c", response.description)
        self.assertEqual(200, response.code)
        self.assertEqual("a", response.message)

    def test_create_from_dictionary__failed_missing_code(self):
        with self.assertRaises(ValueError):
            self.factory.create_from_dictionary({})
