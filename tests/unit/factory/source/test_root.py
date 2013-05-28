import unittest

from mock import patch, call

from apidoc.factory.source.root import Root as RootFactory

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
