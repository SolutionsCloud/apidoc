import unittest

from mock import patch, call

from apidoc.factory.source.element import Element as ElementFactory

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


class TestElement(unittest.TestCase):

    def setUp(self):
        self.factory = ElementFactory()

    def test_set_common_datas__default(self):
        datas = {"description": "c", "sample": "foo"}
        element = Element()
        self.factory.set_common_datas(element, "o_name", datas)

        self.assertEqual("o_name", element.name)
        self.assertEqual("c", element.description)
        self.assertNotIn("display", vars(element))
        self.assertNotIn("sample", vars(element))

    def test_set_common_datas__sampleable(self):
        datas = {"description": "c", "sample": {"foo": "bar"}}
        element = Sampleable()
        self.factory.set_common_datas(element, "o_name", datas)

        self.assertEqual("{'foo': 'bar'}", element.sample)

    def test_set_common_datas__displayable(self):
        datas = {"description": "c", "display": "false"}
        element = Displayable()
        self.factory.set_common_datas(element, "o_name", datas)

        self.assertEqual(False, element.display)

    def test_set_common_datas__displayable_default(self):
        datas = {"description": "c"}
        element = Displayable()
        self.factory.set_common_datas(element, "o_name", datas)

        self.assertEqual(True, element.display)
