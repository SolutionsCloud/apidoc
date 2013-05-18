import unittest

from apidoc.object.source import Root, Element, Sampleable, Displayable, Sortable, ElementCrossVersion
from apidoc.object.source import Version
from apidoc.object.source import Section, Method, Namespace
from apidoc.object.source import Parameter, ResponseCode
from apidoc.object.source import Type, EnumType, EnumTypeValue, TypeFormat
from apidoc.object.source import Object, ObjectObject, ObjectArray
from apidoc.object.source import ObjectNumber, ObjectString, ObjectBool, ObjectNone
from apidoc.object.source import ObjectDynamic, ObjectReference, ObjectType
from apidoc.object.source import MergedMethod, MergedType
from apidoc.object.source import TypeCrossVersion, MethodCrossVersion


class TestSource(unittest.TestCase):

    def test_root_previous_version(self):
        root = Root()
        version1 = Version()
        version2 = Version()
        version1.name = "foo"
        version1.major = 1
        version2.name = "bar"
        version2.major = 2

        root.versions = {"v1": version1, "v2": version2}

        self.assertEqual("foo", root.previous_version("bar"))

    def test_root_previous_version__return_none(self):
        root = Root()
        version1 = Version()
        version2 = Version()
        version1.name = "foo"
        version1.major = 1
        version2.name = "bar"
        version2.major = 2

        root.versions = {"v1": version1, "v2": version2}

        self.assertEqual(None, root.previous_version("foo"))

    def test_root_previous_version__failed_when_wrong_version(self):
        root = Root()
        version1 = Version()
        version1.name = "foo"
        version1.major = 1

        root.versions = {"v1": version1}

        with self.assertRaises(ValueError):
            root.previous_version("baz")

    def test_root_get_used_namespaces(self):
        root = Root.instance()

        namespace1 = Namespace("n1")
        namespace2 = Namespace("n2")

        type1 = Type()
        type2 = Type()

        namespace1.types = {"t1": type1, "t2": type2}
        namespace2.types = {"t2": type2}

        root.namespaces = {"n1": namespace1, "n2": namespace2}

        section = Section()
        method = Method()

        parameter1 = Parameter()
        parameter1.type = "t1"

        method.request_headers = {
            "t1": parameter1
        }

        methodCrossVersion1 = MethodCrossVersion(method)
        methodCrossVersion1.signatures = {"s1" : method}
        section.methods = {"m1": methodCrossVersion1}

        root.sections = {"s1": section}

        response = root.get_used_namespaces()

        self.assertEqual([namespace1], response)

    def test_root_get_used_types(self):
        root = Root.instance()

        namespace1 = Namespace("n1")

        type1 = Type()
        type2 = Type()

        namespace1.types = {"t1": type1, "t2": type2}

        root.namespaces = {"n1": namespace1}

        section = Section()
        method = Method()

        parameter1 = Parameter()
        parameter1.type = "t1"

        method.request_headers = {
            "t1": parameter1
        }

        methodCrossVersion1 = MethodCrossVersion(method)
        methodCrossVersion1.signatures = {"s1" : method}
        section.methods = {"m1": methodCrossVersion1}

        root.sections = {"s1": section}

        response = root.get_used_types()

        self.assertEqual(["t1"], response)

    def test_sampleable_get_sample(self):
        sampleable = Sampleable()
        sampleable.sample = "foo"

        self.assertEqual("foo", sampleable.get_sample())

    def test_sampleable_get_sample__return_default_sample(self):
        sampleable = Sampleable()
        sampleable.sample = None
        sampleable.name = "bar"

        self.assertEqual("my_bar", sampleable.get_sample())

    def test_sortable_compare__with_position(self):
        sortable1 = Sortable()
        sortable2 = Sortable()
        sortable1.name = "a"
        sortable2.name = "b"

        self.assertEqual(sortable1, sorted([sortable2, sortable1])[0])

    def test_sortable_compare__with_name(self):
        sortable1 = Sortable()
        sortable2 = Sortable()
        sortable1.name = "a"
        sortable1.description = "a"
        sortable2.name = "a"
        sortable2.description = "b"

        self.assertEqual(sortable1, sorted([sortable2, sortable1])[0])

    def test_version_full_uri(self):
        Root.instance().configuration.uri = None

        version = Version()
        version.uri = "bar"

        self.assertEqual("bar", version.full_uri)

    def test_method_full_uri__with_root_uri(self):
        Root.instance().configuration.uri = "//foo/"

        version = Version()
        version.uri = "bar"

        self.assertEqual("//foo/bar", version.full_uri)

    def test_method_full_uri__without_version_uri(self):
        Root.instance().configuration.uri = "//foo/"

        version = Version()
        version.uri = None

        self.assertEqual("//foo/", version.full_uri)

    def test_method_full_uri__failled_when_no_version_uri(self):
        Root.instance().configuration.uri = None

        version = Version()
        version.uri = None

        with self.assertRaises(ValueError):
            version.full_uri

    def test_version_compare__with_major(self):
        version1 = Version()
        version2 = Version()
        version1.major = 1
        version2.major = 2

        self.assertEqual(version1, sorted([version2, version1])[0])

    def test_version_compare__with_minor(self):
        version1 = Version()
        version2 = Version()
        version1.major = 1
        version1.minor = 1
        version2.major = 1
        version2.minor = 2

        self.assertEqual(version1, sorted([version2, version1])[0])

    def test_version_compare__with_name(self):
        version1 = Version()
        version2 = Version()
        version1.major = 1
        version1.minor = 1
        version1.name = "a"
        version2.major = 1
        version2.minor = 1
        version2.name = "b"

        self.assertEqual(version1, sorted([version2, version1])[0])

    def test_section_compare__with_order(self):
        section1 = Section()
        section2 = Section()
        section1.order = 1
        section2.order = 2

        self.assertEqual(section1, sorted([section2, section1])[0])

    def test_section_compare__with_name(self):
        section1 = Section()
        section2 = Section()
        section1.order = 1
        section1.name = "a"
        section2.order = 1
        section2.name = "b"

        self.assertEqual(section1, sorted([section2, section1])[0])

    def test_parameter_compare__with_position(self):
        parameter1 = Parameter()
        parameter2 = Parameter()
        parameter1.position = 1
        parameter2.position = 2

        self.assertEqual(parameter1, sorted([parameter2, parameter1])[0])

    def test_parameter_compare__with_name(self):
        parameter1 = Parameter()
        parameter2 = Parameter()
        parameter1.position = 1
        parameter1.name = "a"
        parameter2.position = 1
        parameter2.name = "b"

        self.assertEqual(parameter1, sorted([parameter2, parameter1])[0])

    def test_parameter_compare__with_description(self):
        parameter1 = Parameter()
        parameter2 = Parameter()
        parameter1.position = 1
        parameter1.name = "a"
        parameter1.description = "a"
        parameter2.position = 1
        parameter2.name = "a"
        parameter2.description = "b"

        self.assertEqual(parameter1, sorted([parameter2, parameter1])[0])

    def test_response_code_compare__with_code(self):
        response_code1 = ResponseCode()
        response_code2 = ResponseCode()
        response_code1.code = 1
        response_code2.code = 2

        self.assertEqual(response_code1, sorted([response_code2, response_code1])[0])

    def test_response_code_compare__with_message(self):
        response_code1 = ResponseCode()
        response_code2 = ResponseCode()
        response_code1.code = 1
        response_code1.message = "a"
        response_code2.code = 1
        response_code2.message = "b"

        self.assertEqual(response_code1, sorted([response_code2, response_code1])[0])

    def test_response_code_compare__with_description(self):
        response_code1 = ResponseCode()
        response_code2 = ResponseCode()
        response_code1.code = 1
        response_code1.message = "a"
        response_code1.description = "a"
        response_code2.code = 1
        response_code2.message = "a"
        response_code2.description = "b"

        self.assertEqual(response_code1, sorted([response_code2, response_code1])[0])

    def test_element_get_signature_struct(self):
        test = Element()
        test.name = "foo"
        test.description = "bar"
        self.assertEqual({"name": "foo", "description": "bar"}, test.get_signature_struct())

    def test_displayable_get_signature_struct(self):
        test = Displayable()
        self.assertEqual({"display": True}, test.get_signature_struct())

    def test_method_get_signature_struct(self):
        test = Method()
        test.name = "foo"
        test.description = "bar"
        test.code = 200
        test.uri = "baz/{h1}"
        test.method = Method.Methods("get")
        test.request_headers = {
            "h1": Parameter()
        }
        test.request_parameters = {
            "h1": Parameter(),
            "h2": Parameter()
        }
        test.request_parameters["h1"].name="h1"
        test.request_parameters["h2"].name="h2"
        test.request_body = ObjectNumber()
        test.response_codes = [
            ResponseCode()
        ]
        test.response_body = ObjectNumber()
        self.assertEqual({
            "name": "foo",
            "description": "bar",
            "code": 200,
            "uri": "baz/{h1}",
            "method": "get",
            "request_headers": ['300c4cc6dc22bca7b9e9cb6ba5c7d47c'],
            "request_parameters": ['6987b76282443b02d0ba0154a6a5d3cd'],
            "request_body": 'c570705f2c3228ea10c6bcd485d0c3a7',
            "response_codes": ['198d5b2ef38efed343e6688b1163dd62'],
            "response_body": 'c570705f2c3228ea10c6bcd485d0c3a7',
        }, test.get_signature_struct())

    def test_parameter_get_signature_struct(self):
        test = Parameter()
        test.name = "foo"
        test.description = "bar"
        test.position = 3
        test.type = "baz"

        self.assertEqual({
            "name": "foo",
            "description": "bar",
            "position": 3,
            "type": "baz",
            "optional": False
        }, test.get_signature_struct())

    def test_responsecode_get_signature_struct(self):
        test = ResponseCode()
        test.name = "foo"
        test.description = "bar"
        test.code = 300
        test.message = "baz"

        self.assertEqual({
            "name": "foo",
            "description": "bar",
            "code": 300,
            "message": "baz"
        }, test.get_signature_struct())

    def test_type_get_signature_struct(self):
        test = Type()
        test.name = "foo"
        test.description = "bar"
        test.primary = "baz"
        test.format = TypeFormat()

        self.assertEqual({
            "name": "foo",
            "description": "bar",
            "primary": "baz",
            "format": {'advanced': None, 'pretty': None}
        }, test.get_signature_struct())

    def test_typeformat_get_signature_struct(self):
        test = TypeFormat()
        test.pretty = "foo"
        test.advanced = "bar"

        self.assertEqual({
            "pretty": "foo",
            "advanced": "bar"
        }, test.get_signature_struct())

    def test_enumtype_get_signature_struct(self):
        test = EnumType()
        test.name = "foo"
        test.description = "bar"
        test.primary = "baz"
        test.values = {"v1": EnumTypeValue()}

        self.assertEqual({
            "name": "foo",
            "description": "bar",
            "primary": "baz",
            "format": {'advanced': None, 'pretty': None},
            "values": ["04e6a8f8e40ed17d69647b00a3a62a00"]
        }, test.get_signature_struct())

    def test_object_get_signature_struct(self):
        test = Object()
        test.name = "foo"
        test.description = "bar"
        test.type = Object.Types.number

        self.assertEqual({
            "name": "foo",
            "description": "bar",
            "type": "number",
            "required": True,
            "optional": False
        }, test.get_signature_struct())

    def test_object_unit_signature(self):
        test = Object()
        test.name = "foo"
        test.description = "bar"
        test.type = Object.Types.number

        self.assertEqual("3ce5d9bec0ee76b99df9d60a5c8841c5", test.unit_signature)

    def test_object_get_unit_signature_struct(self):
        test = Object()
        test.name = "foo"
        test.description = "bar"
        test.type = Object.Types.number

        self.assertEqual({
            "description": "bar",
            "type": "number",
            "required": True,
            "optional": False
        }, test.get_unit_signature_struct())

    def test_objectobject_get_signature_struct(self):
        test = ObjectObject()
        test.name = "foo"
        test.description = "bar"
        test.properties = {"bar": Object()}

        self.assertEqual({
            "name": "foo",
            "description": "bar",
            "type": "object",
            "required": True,
            "optional": False,
            "properties": ["4077571d745c363dbd55ee168b0bad28"]
        }, test.get_signature_struct())

    def test_objectobject_get_unit_signature_struct(self):
        test = ObjectObject()
        test.name = "foo"
        test.description = "bar"
        test.properties = {"bar": Object()}

        self.assertEqual({
            "description": "bar",
            "type": "object",
            "required": True,
            "optional": False,
        }, test.get_unit_signature_struct())

    def test_objectobject_get_used_types(self):
        object1 = ObjectType()
        object1.type_name = "t1"

        test = ObjectObject()
        test.properties = {"o1": ObjectString(), "o2": object1}

        self.assertEqual(["t1"], test.get_used_types())

    def test_objectarray_get_signature_struct(self):
        test = ObjectArray()
        test.name = "foo"
        test.description = "bar"
        test.items = Object()

        self.assertEqual({
            "name": "foo",
            "description": "bar",
            "type": "array",
            "required": True,
            "optional": False,
            "items": "4077571d745c363dbd55ee168b0bad28"
        }, test.get_signature_struct())

    def test_objectarray_get_unit_signature_struct(self):
        test = ObjectArray()
        test.name = "foo"
        test.description = "bar"
        test.items = Object()

        self.assertEqual({
            "description": "bar",
            "type": "array",
            "required": True,
            "optional": False,
        }, test.get_unit_signature_struct())

    def test_objectarray_get_used_types(self):
        object1 = ObjectType()
        object1.type_name = "t1"

        test = ObjectArray()
        test.items = object1

        self.assertEqual(["t1"], test.get_used_types())

    def test_objectarray_get_used_types__when_item_is_none(self):
        test = ObjectArray()
        test.items = None

        self.assertEqual([], test.get_used_types())

    def test_objectdynamic_get_signature_struct(self):
        test = ObjectDynamic()
        test.name = "foo"
        test.description = "bar"
        test.items = "baz"

        self.assertEqual({
            "name": "foo",
            "description": "bar",
            "type": "dynamic",
            "required": True,
            "optional": False,
            "items": "baz"
        }, test.get_signature_struct())

    def test_objectdynamic_get_unit_signature_struct(self):
        test = ObjectDynamic()
        test.name = "foo"
        test.description = "bar"
        test.items = "baz"

        self.assertEqual({
            "description": "bar",
            "type": "dynamic",
            "required": True,
            "optional": False,
        }, test.get_unit_signature_struct())

    def test_objectdynamic_get_used_types(self):
        test = ObjectDynamic()
        test.items = "t1"

        self.assertEqual(["t1"], test.get_used_types())
    def test_objectreference_get_signature_struct(self):
        test = ObjectReference()
        test.name = "foo"
        test.description = "bar"
        test.reference_name = "baz"
        test.version = "v1"

        Root.instance().references["baz"] = ElementCrossVersion(Object())
        Root.instance().references["baz"].versions["v1"] = Object()

        self.assertEqual({
            "name": "foo",
            "description": "bar",
            "type": "reference",
            "required": True,
            "optional": False,
            "reference": "4077571d745c363dbd55ee168b0bad28"
        }, test.get_signature_struct())

    def test_objectreference_get_unit_signature_struct(self):
        test = ObjectReference()
        test.name = "foo"
        test.description = "bar"
        test.reference_name = "baz"
        test.version = "v1"

        Root.instance().references["baz"] = ElementCrossVersion(Object())
        Root.instance().references["baz"].versions["v1"] = Object()

        self.assertEqual({
            "description": "bar",
            "type": "reference",
            "required": True,
            "optional": False,
        }, test.get_unit_signature_struct())

    def test_objectreference_get_used_types(self):
        object1 = ObjectType()
        object1.type_name = "t1"

        test = ObjectReference()
        test.reference_name = "baz"
        test.version = "v1"

        Root.instance().references["baz"] = ElementCrossVersion(Object())
        Root.instance().references["baz"].versions["v1"] = object1

        self.assertEqual(["t1"], test.get_used_types())

    def test_objecttype_get_signature_struct(self):
        test = ObjectType()
        test.name = "foo"
        test.description = "bar"
        test.type_name = "baz"
        test.version = "v1"

        Root.instance().types["baz"] = ElementCrossVersion(Type())
        Root.instance().types["baz"].versions["v1"] = Type()

        self.assertEqual({
            "name": "foo",
            "description": "bar",
            "type": "type",
            "required": True,
            "optional": False,
            "type": "fed6dce5e9bbb016ea8d91120c3e1c95"
        }, test.get_signature_struct())

    def test_objecttype_get_unit_signature_struct(self):
        test = ObjectType()
        test.name = "foo"
        test.description = "bar"
        test.type_name = "baz"
        test.version = "v1"

        Root.instance().types["baz"] = ElementCrossVersion(Type())
        Root.instance().types["baz"].versions["v1"] = Type()

        self.assertEqual({
            "name": "foo",
            "description": "bar",
            "type": "type",
            "required": True,
            "optional": False,
            "type": "fed6dce5e9bbb016ea8d91120c3e1c95"
        }, test.get_unit_signature_struct())

    def test_element_version_setter(self):
        section = Section()
        method = Method()
        parameter = Parameter()
        header = Parameter()
        code = ResponseCode()
        request_body = ObjectArray()
        response_body = ObjectObject()
        sub_object = Object()
        sub_array = Object()

        section.methods["m"] = method
        method.request_parameters["p"] = parameter
        method.request_headers["h"] = header
        method.response_codes = [code]
        method.request_body = request_body
        method.response_body = response_body
        response_body.properties["s"] = sub_object
        request_body.items = sub_array

        section.version = "v1"

        self.assertEqual("v1", method.version)
        self.assertEqual("v1", parameter.version)
        self.assertEqual("v1", header.version)
        self.assertEqual("v1", code.version)
        self.assertEqual("v1", response_body.version)
        self.assertEqual("v1", request_body.version)
        self.assertEqual("v1", sub_object.version)
        self.assertEqual("v1", sub_array.version)

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

    def test_method_full_uri(self):
        version = Version()
        version.uri = "foo/"
        Root.instance().versions["v1"] = version

        method = Method()
        method.uri = "bar"
        method.version = "v1"

        self.assertEqual("foo/bar", method.full_uri)

    def test_method_full_uri__with_root_and_version(self):
        Root.instance().configuration.uri = "//foo/"

        version = Version()
        version.uri = "bar/"
        Root.instance().versions["v1"] = version

        method = Method()
        method.uri = "baz"
        method.version = "v1"

        self.assertEqual("//foo/bar/baz", method.full_uri)

    def test_method_full_uri__failled_when_no_version_uri(self):
        version = Version()
        Root.instance().versions["v1"] = version

        method = Method()
        method.uri = "bar"
        method.version = "v1"

        with self.assertRaises(ValueError):
            method.full_uri

    def test_method_cleaned_request_parameters(self):
        method = Method()
        parameter1 = Parameter()
        parameter2 = Parameter()

        method.uri = "bar/{p1}"
        method.request_parameters["p1"] = parameter1
        method.request_parameters["p2"] = parameter2
        parameter1.name = "p1"
        parameter2.name = "p2"

        self.assertEqual({"p1": parameter1}, method.cleaned_request_parameters)

    def test_method_get_used_types(self):
        method = Method()
        parameter1 = Parameter()
        parameter1.name = "p1"
        parameter1.type = "t1"

        parameter1_bad = Parameter()
        parameter1_bad.name = "p1_bad"
        parameter1_bad.type = "t1_bad"

        parameter2 = Parameter()
        parameter2.type = "t2"

        object1 = ObjectType()
        object1.type_name = "t3"

        object2 = ObjectType()
        object2.type_name = "t4"

        method.uri = "bar/{p1}"
        method.request_parameters = {"p1": parameter1, "p1_bad": parameter1_bad}
        method.request_headers = {"p2": parameter2}
        method.request_body = object1
        method.response_body = object2

        self.assertEqual(sorted(["t1", "t2", "t3", "t4"]), sorted(method.get_used_types()))

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
        test.name = "foo"

        self.assertEqual("my_foo", test.get_default_sample())

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

        Root.instance().types["baz"] = ElementCrossVersion(Type())
        Root.instance().types["baz"].versions["v1"] = type

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

    def test_objectreference_get_reference__failed_when_does_not_exists(self):
        test = ObjectReference()
        test.name = "foo"
        test.version = "v1"
        test.reference_name = "bar"

        Root.instance().references = {}

        with self.assertRaises(ValueError):
            test.get_reference()

    def test_objectreference_get_reference__failed_when_version_does_not_exists(self):
        test = ObjectReference()
        test.name = "foo"
        test.version = "v1"
        test.reference_name = "bar"

        Root.instance().references = {
            "bar": ElementCrossVersion(Type())
        }
        Root.instance().references["bar"].versions = {}

        with self.assertRaises(ValueError):
            test.get_reference()

    def test_objecttype_get_type__failed_when_does_not_exists(self):
        test = ObjectType()
        test.name = "foo"
        test.version = "v1"
        test.type_name = "bar"

        Root.instance().types = {}

        with self.assertRaises(ValueError):
            test.get_type()

    def test_objecttype_get_type__failed_when_version_does_not_exists(self):
        test = ObjectType()
        test.name = "foo"
        test.version = "v1"
        test.type_name = "bar"

        Root.instance().types = {
            "bar": ElementCrossVersion(Type())
        }
        Root.instance().types["bar"].versions = {}

        with self.assertRaises(ValueError):
            test.get_type()

    def test_elementCrossVersion_changed_status(self):
        version1 = Version()
        version2 = Version()
        version3 = Version()
        version1.name = "v1"
        version1.major = 1
        version2.name = "v2"
        version2.major = 2
        version3.name = "v3"
        version3.major = 3

        Root.instance().versions = {
            "v1": version1,
            "v2": version2,
            "v3": version3
        }

        test = ElementCrossVersion(Method())
        self.assertEqual(ElementCrossVersion.Change.none, test.changed_status("v1"))

        test.versions = {"v1": Method()}
        self.assertEqual(ElementCrossVersion.Change.new, test.changed_status("v1"))

        test.versions = {}
        self.assertEqual(ElementCrossVersion.Change.none, test.changed_status("v2"))

        test.versions = {"v2": Method()}
        self.assertEqual(ElementCrossVersion.Change.new, test.changed_status("v2"))

        test.versions = {"v1": Method()}
        self.assertEqual(ElementCrossVersion.Change.deleted, test.changed_status("v2"))

        test.versions = {"v1": Method(), "v2": Method()}
        test.versions["v1"].name = "foo"
        test.versions["v2"].name = "bar"

        self.assertEqual(ElementCrossVersion.Change.updated, test.changed_status("v2"))

        test.versions = {"v1": Method(), "v2": Method()}
        self.assertEqual(ElementCrossVersion.Change.none, test.changed_status("v2"))

    def test_mergedMethod(self):
        test = MergedMethod();

        self.assertIsInstance(test.description, list)
        self.assertIsInstance(test.full_uri, list)
        self.assertIsInstance(test.request_parameters, list)
        self.assertIsInstance(test.request_headers, list)
        self.assertIsInstance(test.request_body, list)
        self.assertIsInstance(test.response_body, list)
        self.assertIsInstance(test.response_codes, list)

    def test_mergedType(self):
        test = MergedType();

        self.assertIsInstance(test.description, list)
        self.assertIsInstance(test.primary, list)
        self.assertIsInstance(test.values, list)

    def test_typeCrossVersion_merged(self):
        version1 = Version()
        version2 = Version()
        version3 = Version()

        value1 = EnumTypeValue()
        value1.name = "foo"
        value2 = EnumTypeValue()
        value2.name = "bar"

        type1 = Type()
        type1.description = "foo"
        type1.primary = Type.Primaries.enum
        type1.values = {"foo": value1, "bar": value2}

        type2 = Type()
        type2.description = "foo"
        type2.primary = Type.Primaries.enum
        type2.values = {}

        type3 = Type()
        type3.description = "bar"
        type3.primary = Type.Primaries.enum
        type3.values = {"foo": value1}

        test = TypeCrossVersion(type1)

        test.versions = {"v1": type1, "v2": type2, "v3": type3}
        merged = test.merged

        self.assertIsInstance(merged, MergedType)
        self.assertEqual(["foo", "bar"], merged.description)
        self.assertEqual([Type.Primaries.enum], merged.primary)
        self.assertEqual([value1, value2], merged.values)

    def test_methodCrossVersion_merged(self):
        version1 = Version()
        version1.uri = "foo/"
        version2 = Version()
        version2.uri = "foo/"
        version3 = Version()
        version3.uri = "foo/"

        parameter_test = Parameter()
        parameter_test.name = "test"
        parameter_foo = Parameter()
        parameter_foo.name = "foo"

        response_200 = ResponseCode()
        response_200.code = 200
        response_404 = ResponseCode()
        response_404.code = 404
        response_404.description = "global"
        response_404_s = ResponseCode()
        response_404_s.code = 404
        response_404_s.description = "specific"

        method1 = Method()
        method1.version = "v1"
        method1.description = "foo"
        method1.uri = "foo{test}"
        method1.request_parameters = {"test": parameter_test}
        method1.request_headers = {"test": parameter_test}
        method1.response_codes = [response_200]
        method1.request_body = "foo"
        method1.response_body = "foo"

        method2 = Method()
        method2.version = "v2"
        method2.description = "foo"
        method2.uri = "bar{test}"
        method2.request_parameters = {"test": parameter_test, "foo": parameter_foo}
        method2.response_codes = [response_200, response_404]
        method2.request_body = "bar"
        method2.request_body = "bar"

        method3 = Method()
        method3.version = "v3"
        method3.description = "bar"
        method3.uri = "baz"
        method3.request_headers = {"foo": parameter_foo}
        method3.response_codes = [response_404, response_404_s]
        method3.response_body = "foo"
        method3.response_body = "bar"

        Root.instance().versions = {
            "v1": version1,
            "v2": version2,
            "v3": version3
        }

        test = MethodCrossVersion(method1)

        test.versions = {"v1": method1, "v2": method2, "v3": method3}
        merged = test.merged

        self.assertIsInstance(merged, MergedMethod)
        self.assertEqual(["foo", "bar"], merged.description)
        self.assertEqual(["foo/foo{test}", "foo/bar{test}", "foo/baz"], merged.full_uri)
        self.assertEqual([parameter_test], merged.request_parameters)
        self.assertEqual([parameter_test, parameter_foo], merged.request_headers)
        self.assertEqual([response_200, response_404, response_404_s], merged.response_codes)
        self.assertEqual(["foo", "bar"], merged.request_body)
        self.assertEqual(["foo", "bar"], merged.response_body)

    def test_methodCrossVersion_objects_without_reference(self):
        method = Method()
        test = MethodCrossVersion(method)

        object1 = ObjectObject()

        object2 = ObjectReference()
        object2.version = "v1"
        object2.reference_name = "baz"

        reference1 = ObjectObject()

        Root.instance().references = {
            "baz": ElementCrossVersion(Type())
        }
        Root.instance().references["baz"].versions = {"v1": reference1}

        response = test.objects_without_reference([object1, object2])
        self.assertEqual([object1, reference1], response)

    def test_methodCrossVersion_objects_by_unit_signature(self):
        method = Method()
        test = MethodCrossVersion(method)

        object1 = Object()
        object1._unit_signature = "s1"
        object1.version = "v1"

        object2 = Object()
        object2._unit_signature = "s2"
        object2.version = "v2"

        object3 = Object()
        object3._unit_signature = "s1"
        object3.version = "v3"

        response = test.objects_by_unit_signature([object1, object2, object3])
        self.assertEqual(2, len(response))
        self.assertEqual(["v1", "v3"], response[0].versions)
        self.assertEqual(["v2"], response[1].versions)

    def test_methodCrossVersion_objects_merge_properties(self):
        method = Method()
        test = MethodCrossVersion(method)

        object1 = ObjectObject()
        object1.properties = {"foo": "bar"}

        object2 = ObjectObject()
        object2.properties = {"baz": "qux"}

        object3 = ObjectObject()
        object3.properties = {"foo": "fum"}

        response = test.objects_merge_properties([object1, object2, object3])
        self.assertEqual({"foo": "bar", "baz": "qux"}, response)

    def test_methodCrossVersion_objects_property_by_property_name(self):
        method = Method()
        test = MethodCrossVersion(method)

        object1 = ObjectObject()
        object1.properties = {"foo": "bar"}

        object2 = ObjectObject()
        object2.properties = {"baz": "qux"}

        object3 = ObjectObject()
        object3.properties = {"foo": "fum"}

        response = test.objects_property_by_property_name([object1, object2, object3], "foo")
        self.assertEqual(["bar", "fum"], response)

    def test_methodCrossVersion_objects_items(self):
        method = Method()
        test = MethodCrossVersion(method)

        object1 = ObjectArray()
        object1.items = "foo"

        object2 = ObjectArray()
        object2.items = "baz"

        object3 = ObjectArray()
        object3.items = "foo"

        response = test.objects_items([object1, object2, object3])
        self.assertEqual(["foo", "baz", "foo"], response)

    def test_methodCrossVersion_objects_reference(self):
        method = Method()
        test = MethodCrossVersion(method)

        object1 = ObjectReference()
        object1.version = "v1"
        object1.reference_name = "foo"

        object2 = ObjectReference()
        object2.version = "v1"
        object2.reference_name = "baz"

        object3 = ObjectReference()
        object3.version = "v1"
        object3.reference_name = "foo"

        reference1 = ObjectObject()
        reference2 = ObjectObject()

        Root.instance().references = {
            "foo": ElementCrossVersion(Type()),
            "baz": ElementCrossVersion(Type())
        }
        Root.instance().references["foo"].versions = {"v1": reference1}
        Root.instance().references["baz"].versions = {"v1": reference2}

        response = test.objects_reference([object1, object2, object3])
        self.assertEqual([reference1, reference2, reference1], response)

