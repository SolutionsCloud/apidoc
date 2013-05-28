import unittest

from mock import patch, call

from apidoc.factory.source.category import Category as CategoryFactory

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


class TestCategory(unittest.TestCase):

    def setUp(self):
        self.factory = CategoryFactory()

    def test_create_from_name_and_dictionary(self):
        datas = {
            "description": "c",
            "order": "10"
        }
        response = self.factory.create_from_name_and_dictionary("o_name", datas)

        self.assertIsInstance(response, Category)
        self.assertEqual("o_name", response.name)
        self.assertEqual("c", response.description)
