import unittest

from apidoc.factory.source.method import Method as MethodFactory

from apidoc.object.source_raw import Method, Parameter, ObjectString, ObjectNumber


class TestMethod(unittest.TestCase):

    def setUp(self):
        self.factory = MethodFactory()

    def test_create_from_name_and_dictionary(self):
        datas = {
            "description": "c",
            "code": "302",
            "category": "y",
            "uri": "a",
            "method": "put",
            "request_headers": {"h_name": {}},
            "request_parameters": {"p_name": {}},
            "response_codes": [{"code": "302"}],
            "request_body": {"type": "string"},
            "response_body": {"type": "number"}
        }
        response = self.factory.create_from_name_and_dictionary("o_name", datas)

        self.assertIsInstance(response, Method)
        self.assertEqual("o_name", response.name)
        self.assertEqual("y", response.category)
        self.assertEqual("c", response.description)
        self.assertEqual(302, response.code)
        self.assertEqual("a", response.uri)
        self.assertIsInstance(response.method, Method.Methods)
        self.assertEqual("put", str(response.method))
        self.assertIn("h_name", response.request_headers)
        self.assertIsInstance(response.request_headers["h_name"], Parameter)
        self.assertEqual("h_name", response.request_headers["h_name"].name)
        self.assertIn("p_name", response.request_parameters)
        self.assertIsInstance(response.request_parameters["p_name"], Parameter)
        self.assertEqual("p_name", response.request_parameters["p_name"].name)
        self.assertIsInstance(response.request_body, ObjectString)
        self.assertIsInstance(response.response_codes, list)
        self.assertIsInstance(response.response_body, ObjectNumber)
        self.assertEqual(1, len(response.response_codes))

    def test_create_from_name_and_dictionary__method_get(self):
        datas = {
            "method": "get",
        }
        response = self.factory.create_from_name_and_dictionary("o_name", datas)

        self.assertIsInstance(response, Method)
        self.assertEqual(Method.Methods.get, response.method)

    def test_create_from_name_and_dictionary__method_post(self):
        datas = {
            "method": "post",
        }
        response = self.factory.create_from_name_and_dictionary("o_name", datas)

        self.assertIsInstance(response, Method)
        self.assertEqual(Method.Methods.post, response.method)

    def test_create_from_name_and_dictionary__method_put(self):
        datas = {
            "method": "put",
        }
        response = self.factory.create_from_name_and_dictionary("o_name", datas)

        self.assertIsInstance(response, Method)
        self.assertEqual(Method.Methods.put, response.method)

    def test_create_from_name_and_dictionary__method_delete(self):
        datas = {
            "method": "delete",
        }
        response = self.factory.create_from_name_and_dictionary("o_name", datas)

        self.assertIsInstance(response, Method)
        self.assertEqual(Method.Methods.delete, response.method)

    def test_create_from_name_and_dictionary__method_patch(self):
        datas = {
            "method": "patch",
        }
        response = self.factory.create_from_name_and_dictionary("o_name", datas)

        self.assertIsInstance(response, Method)
        self.assertEqual(Method.Methods.patch, response.method)

    def test_create_from_name_and_dictionary__method_head(self):
        datas = {
            "method": "head",
        }
        response = self.factory.create_from_name_and_dictionary("o_name", datas)

        self.assertIsInstance(response, Method)
        self.assertEqual(Method.Methods.head, response.method)

    def test_create_from_name_and_dictionary__method_option(self):
        datas = {
            "method": "option",
        }
        response = self.factory.create_from_name_and_dictionary("o_name", datas)

        self.assertIsInstance(response, Method)
        self.assertEqual(Method.Methods.option, response.method)

    def test_create_from_name_and_dictionary__failed_wrong_method(self):
        with self.assertRaises(ValueError):
            self.factory.create_from_name_and_dictionary("o_name", {"method": "foo"})
