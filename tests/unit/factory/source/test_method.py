import unittest

from mock import patch, call

from apidoc.factory.source.method import Method as MethodFactory

from apidoc.object.config import Config as ConfigObject

from apidoc.object.source import Root, Element, Sampleable, Displayable
from apidoc.object.source import Version, Configuration
from apidoc.object.source import MethodCategory, Method, Category, TypeCategory
from apidoc.object.source import Parameter, ResponseCode
from apidoc.object.source import Type, EnumType, EnumTypeValue, TypeFormat
from apidoc.object.source import Object, ObjectObject, ObjectArray
from apidoc.object.source import ObjectNumber, ObjectString, ObjectBool, ObjectNone
from apidoc.object.source import ObjectDynamic, ObjectReference, ObjectType

from apidoc.service.parser import Parser
from apidoc.service.merger import Merger
from apidoc.service.extender import Extender


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

    def test_create_from_name_and_dictionary__failed_wrong_method(self):
        with self.assertRaises(ValueError):
            self.factory.create_from_name_and_dictionary("o_name", {"method": "foo"})
