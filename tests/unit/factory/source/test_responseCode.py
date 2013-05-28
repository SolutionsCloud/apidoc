import unittest

from mock import patch, call

from apidoc.factory.source.responseCode import ResponseCode as ResponseCodeFactory

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