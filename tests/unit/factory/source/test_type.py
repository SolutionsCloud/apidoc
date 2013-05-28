import unittest

from mock import patch, call

from apidoc.factory.source.type import Type as TypeFactory

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


class TestType(unittest.TestCase):

    def setUp(self):
        self.factory = TypeFactory()

    def test_create_from_name_and_dictionary(self):
        datas = {
            "primary": "string",
            "description": "c",
            "category": "a",
            "format": {
                "pretty": "p",
                "sample": "s",
                "advanced": "d",
            }
        }
        response = self.factory.create_from_name_and_dictionary("o_name", datas)

        self.assertIsInstance(response, Type)
        self.assertEqual("o_name", response.name)
        self.assertEqual("c", response.description)
        self.assertIsInstance(response.primary, Type.Primaries)
        self.assertEqual("string", str(response.primary))
        self.assertIsInstance(response.format, TypeFormat)
        self.assertEqual("p", response.format.pretty)
        self.assertEqual("s", response.format.sample)
        self.assertEqual("d", response.format.advanced)

    def test_create_from_name_and_dictionary__failed_missing_primary(self):
        with self.assertRaises(ValueError):
            self.factory.create_from_name_and_dictionary("o_name", {})

    def test_create_from_name_and_dictionary__failed_wrong_primary(self):
        with self.assertRaises(ValueError):
            self.factory.create_from_name_and_dictionary("o_name", {"primary": "foo"})

    def test_create_from_name_and_dictionary__enum(self):
        datas = {
            "primary": "enum",
            "values": {"a": {"description": "b"}}
        }
        response = self.factory.create_from_name_and_dictionary("o_name", datas)

        self.assertIsInstance(response, EnumType)
        self.assertIsInstance(response.primary, Type.Primaries)
        self.assertEqual("enum", str(response.primary))
        self.assertIn("a", response.values)
        self.assertIsInstance(response.values["a"], EnumTypeValue)
        self.assertEqual("a", response.values["a"].name)

    def test_create_from_name_and_dictionary__enum__failed_missing_primary(self):
        with self.assertRaises(ValueError):
            self.factory.create_from_name_and_dictionary("o_name", {})

    def test_create_from_name_and_dictionary__enum__failed_wrong_primary(self):
        with self.assertRaises(ValueError):
            self.factory.create_from_name_and_dictionary("o_name", {"primary": "foo"})