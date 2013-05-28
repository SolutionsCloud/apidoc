import unittest

from mock import patch, call

from apidoc.factory.source.parameter import Parameter as ParameterFactory

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