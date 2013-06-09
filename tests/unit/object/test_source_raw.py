import unittest

from apidoc.object.source_raw import Root, Element, Sampleable, Displayable
from apidoc.object.source_raw import Root as RootDto
from apidoc.object.source_raw import Version
from apidoc.object.source_raw import Method, Category
from apidoc.object.source_raw import Parameter, ResponseCode
from apidoc.object.source_raw import Type, EnumType, EnumTypeValue, TypeFormat
from apidoc.object.source_raw import Object, ObjectObject, ObjectArray
from apidoc.object.source_raw import ObjectNumber, ObjectString, ObjectBool, ObjectNone
from apidoc.object.source_raw import ObjectDynamic, ObjectReference, ObjectType


class TestSource(unittest.TestCase):

    def test_sampleable_get_sample(self):
        sampleable = Sampleable()
        sampleable.sample = "foo"

        self.assertEqual("foo", sampleable.get_sample())

    def test_sampleable_get_sample__return_default_sample(self):
        sampleable = Sampleable()
        sampleable.sample = None
        sampleable.name = "bar"

        self.assertEqual("my_bar", sampleable.get_sample())

    def test_type_get_sample(self):
        type = Type()
        type.format.sample = "foo"

        self.assertEqual("foo", type.get_sample())

    def test_type_get_sample__return_default_sample(self):
        type = Type()
        type.format.sample = None
        type.name = "bar"

        self.assertEqual("my_bar", type.get_sample())

    def test_enum_type_get_sample__return_first_value(self):
        type = EnumType()
        type.format.sample = None

        value1 = EnumTypeValue()
        value1.name = "foo"
        value2 = EnumTypeValue()
        value2.name = "bar"

        type.values = {"foo": value1, "bar": value2}
        type.name = "bar"

        self.assertEqual("foo", type.get_sample())

    def test_enum_type_get_sample__return_default_sample(self):
        type = EnumType()
        type.format.sample = None

        type.values = {}
        type.name = "bar"

        self.assertEqual("my_bar", type.get_sample())

    def test_method_message(self):
        method = Method()
        code = ResponseCode()
        code.code = 100
        code.message = "foo"

        method.code = 100
        method.response_codes = [code]

        self.assertEqual("foo", method.message)

    def test_method_message__ok(self):
        method = Method()

        method.code = 200

        self.assertEqual("OK", method.message)

    def test_method_message__failled_when_no_code_found(self):
        method = Method()
        code = ResponseCode()
        code.code = 100
        code.message = "foo"

        method.code = 300
        method.response_codes = [code]

        with self.assertRaises(ValueError):
            method.message

    def test_sampleable_get_default_sample(self):
        test = Sampleable()
        test.name = "foo"

        self.assertEqual("my_foo", test.get_default_sample())

    def test_parameter_get_default_sample(self):
        test = Parameter()
        test.type = "number"

        self.assertEqual("123", test.get_default_sample())

    def test_typeformat_get_default_sample(self):
        test = TypeFormat()
        test.pretty = "foo"

        self.assertEqual("foo", test.get_default_sample())

    def test_typeformat_get_default_sample__pretty_undefined(self):
        test = TypeFormat()

        self.assertEqual(None, test.get_default_sample())

    def test_objectnumber_get_default_sample(self):
        test = ObjectNumber()

        self.assertEqual('123', test.get_default_sample())

    def test_objectbool_get_default_sample(self):
        test = ObjectBool()

        self.assertEqual('true', test.get_default_sample())

    def test_objectdynamic_get_default_sample(self):
        test = ObjectDynamic()
        test.name = "foo"

        self.assertEqual({
            "key1": "my_foo",
            "key2": "sample"
        }, test.get_default_sample())

    def test_objecttype_get_default_sample(self):
        test = ObjectType()
        test.version = "v1"
        test.type_name = "baz"

        type = Type()
        type.format = TypeFormat()
        type.format.pretty = "foo"

        test.items = type
        print(type.get_sample())

        self.assertEqual("foo", test.get_default_sample())

    def test_object_factory(self):
        self.assertIsInstance(Object.factory("object", "v1"), ObjectObject)
        self.assertIsInstance(Object.factory("array", "v1"), ObjectArray)
        self.assertIsInstance(Object.factory("number", "v1"), ObjectNumber)
        self.assertIsInstance(Object.factory("string", "v1"), ObjectString)
        self.assertIsInstance(Object.factory("bool", "v1"), ObjectBool)
        self.assertIsInstance(Object.factory("reference", "v1"), ObjectReference)
        self.assertIsInstance(Object.factory("type", "v1"), ObjectType)
        self.assertIsInstance(Object.factory("none", "v1"), ObjectNone)
        self.assertIsInstance(Object.factory("dynamic", "v1"), ObjectDynamic)

    def test_object_factory_link(self):
        response = Object.factory("foo", "v1")

        self.assertIsInstance(response, ObjectType)
        self.assertEqual("foo", response.type_name)
