import unittest

from apidoc.object.source_raw import Sampleable
from apidoc.object.source_raw import Method
from apidoc.object.source_raw import Parameter, ResponseCode
from apidoc.object.source_raw import Type, TypeFormat
from apidoc.object.source_raw import Object, ObjectObject, ObjectArray
from apidoc.object.source_raw import ObjectNumber, ObjectString, ObjectBool, ObjectNone
from apidoc.object.source_raw import ObjectDynamic, ObjectReference, ObjectType, ObjectConst, ObjectEnum, EnumValue
from apidoc.object.source_raw import Object as ObjectRaw


class TestSourceRaw(unittest.TestCase):

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
        type.item = ObjectString()
        type.item.name = "a"

        self.assertEqual("my_a", type.get_sample())

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

    def test_parameter_get_default_sample__for_type(self):
        test = Parameter()

        type = Type()
        type.item = ObjectString()
        type.item.name = "a"

        test.type = "b"
        test.type_object = type

        self.assertEqual("my_a", test.get_default_sample())

    def test_objectnumber_get_default_sample(self):
        test = ObjectNumber()

        self.assertEqual('123', test.get_default_sample())

    def test_objectbool_get_default_sample(self):
        test = ObjectBool()

        self.assertEqual('True', str(test.get_default_sample()))

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

        object = ObjectString()
        object.sample = "foo"

        type = Type()
        type.format = TypeFormat()
        type.item = object

        test.type_object = type

        self.assertEqual("foo", test.get_default_sample())

    def test_objectconst_get_default_sample(self):
        test = ObjectConst()
        test.value = "foo"

        self.assertEqual("foo", test.get_default_sample())

    def test_object_factory(self):
        ObjectRaw.Types.foo = "foo"

        self.assertIsInstance(Object.factory("object", "v1"), ObjectObject)
        self.assertIsInstance(Object.factory("array", "v1"), ObjectArray)
        self.assertIsInstance(Object.factory("number", "v1"), ObjectNumber)
        self.assertIsInstance(Object.factory("string", "v1"), ObjectString)
        self.assertIsInstance(Object.factory("bool", "v1"), ObjectBool)
        self.assertIsInstance(Object.factory("reference", "v1"), ObjectReference)
        self.assertIsInstance(Object.factory("type", "v1"), ObjectType)
        self.assertIsInstance(Object.factory("none", "v1"), ObjectNone)
        self.assertIsInstance(Object.factory("dynamic", "v1"), ObjectDynamic)
        self.assertIsInstance(Object.factory("foo", "v1"), ObjectRaw)

        del ObjectRaw.Types.foo

    def test_objectenum__get_default_sample(self):
        test = ObjectEnum()
        test.values = ["foo"]

        self.assertEqual("foo", test.get_default_sample())

    def test_objectconst__fallback(self):
        test = ObjectEnum()
        test.name = "a"

        self.assertEqual("my_a", test.get_default_sample())

    def test_enum_value_compare__with_name(self):
        value1 = EnumValue()
        value2 = EnumValue()
        value1.name = "a"
        value2.name = "b"

        self.assertTrue(value1 < value2)

    def test_enum_value_compare__with_description(self):
        value1 = EnumValue()
        value2 = EnumValue()
        value1.name = "a"
        value1.description = "a"
        value2.name = "a"
        value2.description = "b"

        self.assertTrue(value1 < value2)
