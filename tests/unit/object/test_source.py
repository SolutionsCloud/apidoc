import unittest

from apidoc.object.source import Root, Element, Sampleable, Displayable, Sortable, ElementCrossVersion
from apidoc.object.source import Version
from apidoc.object.source import Section, Method
from apidoc.object.source import Parameter, ResponseCode
from apidoc.object.source import Type, EnumType, EnumTypeValue, TypeFormat
from apidoc.object.source import Object, ObjectObject, ObjectArray
from apidoc.object.source import ObjectNumber, ObjectString, ObjectBool, ObjectNone
from apidoc.object.source import ObjectDynamic, ObjectReference, ObjectType


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
        test.uri = "baz"
        test.method = Method.Methods("get")
        test.request_headers = {
            "h1": Parameter()
        }
        test.request_parameters = {
            "h1": Parameter()
        }
        test.request_body = ObjectNumber()
        test.response_codes = [
            ResponseCode()
        ]
        test.response_body = ObjectNumber()
        self.assertEqual({
            "name": "foo",
            "description": "bar",
            "code": 200,
            "uri": "baz",
            "method": "get",
            "request_headers": ['f55ac54465f03343868b89376fa312ac'],
            "request_parameters": ['f55ac54465f03343868b89376fa312ac'],
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

    def test_objectdynamic_get_signature_struct(self):
        test = ObjectDynamic()
        test.name = "foo"
        test.description = "bar"
        test.itemType = "baz"

        self.assertEqual({
            "name": "foo",
            "description": "bar",
            "type": "dynamic",
            "required": True,
            "optional": False,
            "itemType": "baz"
        }, test.get_signature_struct())

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
