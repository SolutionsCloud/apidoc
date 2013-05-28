import unittest

from mock import patch, call

from apidoc.factory.source.configuration import Configuration as ConfigurationFactory

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
