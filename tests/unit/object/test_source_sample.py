import unittest

from apidoc.object.source_raw import Type
from apidoc.object.source_sample import Type as TypeSample
from apidoc.object.source_raw import Method
from apidoc.object.source_sample import Method as MethodSample
from apidoc.object.source_raw import Parameter, ObjectObject, ObjectArray, ObjectType, ObjectDynamic, Object, ObjectConst, ObjectString
from apidoc.object.source_sample import Parameter as ParameterSample
from apidoc.object.source_sample import ObjectObject as ObjectObjectSample
from apidoc.object.source_sample import ObjectArray as ObjectArraySample
from apidoc.object.source_sample import Object as ObjectSample
from apidoc.object.source_sample import ObjectType as ObjectTypeSample
from apidoc.object.source_sample import ObjectDynamic as ObjectDynamicSample
from apidoc.object.source_sample import ObjectConst as ObjectConstSample
from apidoc.object.source_sample import ObjectEnum as ObjectEnumSample


class TestSourceSample(unittest.TestCase):

    def test_type(self):
        type = Type()
        type.name = "a"
        type.format.pretty = "c"
        type.format.advanced = "d"

        type_sample = TypeSample(type)

        self.assertEqual("a", type_sample.name)
        self.assertEqual("my_a", type_sample.sample)
        self.assertEqual("c", type_sample.pretty)
        self.assertEqual("d", type_sample.advanced)

    def test_method(self):
        method = Method()
        method.name = "a"
        method.method = Method.Methods.post
        method.code = 200
        method.full_uri = "c"
        method.absolute_uri = "d"

        parameter = Parameter()
        parameter.type = "string"
        method.request_headers = {"e": parameter}
        method.request_parameters = {"f": parameter}
        method.request_body = ObjectObject()
        method.response_body = ObjectArray()

        method_sample = MethodSample(method)

        self.assertEqual("a", method_sample.name)
        self.assertEqual(Method.Methods.post, method_sample.method)
        self.assertEqual(200, method_sample.code)
        self.assertEqual("OK", method_sample.message)
        self.assertEqual("c", method_sample.full_uri)
        self.assertEqual("d", method_sample.absolute_uri)
        self.assertIsInstance(method_sample.request_headers, list)
        self.assertEqual(1, len(method_sample.request_headers))
        self.assertIsInstance(method_sample.request_headers[0], ParameterSample)
        self.assertIsInstance(method_sample.request_parameters, dict)
        self.assertEqual(1, len(method_sample.request_parameters.values()))
        self.assertIsInstance(method_sample.request_parameters["f"], ParameterSample)
        self.assertIsInstance(method_sample.request_body, ObjectObjectSample)
        self.assertIsInstance(method_sample.response_body, ObjectArraySample)

    def test_method_compare__with_name(self):
        method_sample1 = MethodSample(Method())
        method_sample2 = MethodSample(Method())

        method_sample1.name = "a"
        method_sample2.name = "b"

        self.assertTrue(method_sample1 < method_sample2)

    def test_parameter(self):
        parameter = Parameter()
        parameter.name = "a"
        parameter.type = "string"
        parameter.optional = True
        parameter.position = 0

        parameter_sample = ParameterSample(parameter)

        self.assertEqual("a", parameter_sample.name)
        self.assertTrue(parameter_sample.optional)
        self.assertEqual("my_a", parameter_sample.sample)
        self.assertFalse(parameter_sample.is_query_string)

    def test_object_factory(self):
        self.assertIsInstance(ObjectSample.factory(Object.factory("object", "v1")), ObjectObjectSample)
        self.assertIsInstance(ObjectSample.factory(Object.factory("array", "v1")), ObjectArraySample)
        self.assertIsInstance(ObjectSample.factory(Object.factory("number", "v1")), ObjectSample)
        self.assertIsInstance(ObjectSample.factory(Object.factory("string", "v1")), ObjectSample)
        self.assertIsInstance(ObjectSample.factory(Object.factory("boolean", "v1")), ObjectSample)
        self.assertIsInstance(ObjectSample.factory(Object.factory("type", "v1")), ObjectTypeSample)
        self.assertIsInstance(ObjectSample.factory(Object.factory("none", "v1")), ObjectSample)
        self.assertIsInstance(ObjectSample.factory(Object.factory("dynamic", "v1")), ObjectDynamicSample)
        self.assertIsInstance(ObjectSample.factory(Object.factory("const", "v1")), ObjectConstSample)
        self.assertIsInstance(ObjectSample.factory(Object.factory("enum", "v1")), ObjectEnumSample)

    def test_object(self):
        object = Object()
        object.name = "a"
        object.type = Object.Types.string
        object.optional = True

        object_sample = ObjectSample(object)

        self.assertEqual("a", object_sample.name)
        self.assertEqual(Object.Types.string, object_sample.type)
        self.assertTrue(object_sample)
        self.assertEqual("my_a", object_sample.sample)

    def test_objectObject(self):
        object = ObjectObject()
        object.name = "a"
        object.type = Object.Types.object

        object2 = ObjectArray()
        object2.name = "b"
        object2.type = Object.Types.array

        object.properties = {"b": object2}

        object_sample = ObjectObjectSample(object)

        self.assertEqual("a", object_sample.name)
        self.assertIsInstance(object_sample.properties, dict)
        self.assertEqual(1, len(object_sample.properties))
        self.assertIsInstance(object_sample.properties["b"], ObjectArraySample)

    def test_objectArray(self):
        object = ObjectArray()
        object.name = "a"
        object.sample_count = 1
        object.type = Object.Types.array

        object2 = ObjectArray()
        object2.name = "b"
        object2.type = Object.Types.array

        object.items = object2

        object_sample = ObjectArraySample(object)

        self.assertEqual("a", object_sample.name)
        self.assertEqual(1, object_sample.sample_count)
        self.assertIsInstance(object_sample.items, ObjectArraySample)

    def test_objectDynamic(self):
        object = ObjectDynamic()
        object.name = "a"
        object.type = Object.Types.dynamic

        object2 = ObjectDynamic()
        object2.name = "b"
        object2.type = Object.Types.dynamic

        object.items = object2

        object_sample = ObjectDynamicSample(object)

        self.assertEqual("a", object_sample.name)
        self.assertIsInstance(object_sample.items, ObjectDynamicSample)

    def test_objectConst(self):
        object = ObjectConst()
        object.name = "a"
        object.const_type = ObjectConst.Types.number
        object.value = 21

        object_sample = ObjectConstSample(object)

        self.assertEqual("a", object_sample.name)
        self.assertEqual(ObjectConst.Types.number, object_sample.const_type)
        self.assertEqual(21, object_sample.value)

    def test_objectType(self):
        object = ObjectType()
        object.name = "a"
        object.type = Object.Types.type
        object.type_object = Type()
        object.type_object.item = ObjectString()

        object_sample = ObjectTypeSample(object)

        self.assertEqual("a", object_sample.name)
