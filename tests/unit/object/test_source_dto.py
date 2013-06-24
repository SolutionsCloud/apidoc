import unittest

from apidoc.object.source_dto import Root as RootDto
from apidoc.object.source_dto import Category as CategoryDto
from apidoc.object.source_raw import Category
from apidoc.object.source_dto import TypeCategory as TypeCategoryDto
from apidoc.object.source_dto import MethodCategory as MethodCategoryDto
from apidoc.object.source_dto import Version as VersionDto
from apidoc.object.source_raw import Version
from apidoc.object.source_dto import Parameter as ParameterDto
from apidoc.object.source_dto import PositionableParameter as PositionableParameterDto
from apidoc.object.source_raw import Parameter
from apidoc.object.source_dto import Method as MethodDto
from apidoc.object.source_raw import Method
from apidoc.object.source_dto import Type as TypeDto
from apidoc.object.source_raw import Type
from apidoc.object.source_dto import EnumTypeValue as EnumTypeValueDto
from apidoc.object.source_raw import EnumTypeValue
from apidoc.object.source_dto import TypeFormat as TypeFormatDto
from apidoc.object.source_raw import TypeFormat
from apidoc.object.source_dto import Object as ObjectDto
from apidoc.object.source_raw import Object
from apidoc.object.source_dto import Element as ElementDto
from apidoc.object.source_raw import Element
from apidoc.object.source_dto import ElementVersioned as ElementVersionedDto
from apidoc.object.source_dto import MultiVersion as MultiVersionDto
from apidoc.object.source_dto import ResponseCode as ResponseCodeDto
from apidoc.object.source_raw import ResponseCode, ObjectType
from apidoc.object.source_dto import ObjectObject as ObjectObjectDto
from apidoc.object.source_dto import ObjectArray as ObjectArrayDto
from apidoc.object.source_dto import ObjectType as ObjectTypeDto
from apidoc.object.source_dto import ObjectDynamic as ObjectDynamicDto
from apidoc.object.source_raw import ObjectConst
from apidoc.object.source_dto import ObjectConst as ObjectConstDto


class TestSourceDto(unittest.TestCase):

    def test_root(self):
        root_dto = RootDto()

        self.assertEqual(None, root_dto.configuration)
        self.assertEqual([], root_dto.versions)
        self.assertEqual([], root_dto.method_categories)
        self.assertEqual([], root_dto.type_categories)

    def test_element(self):
        element = Element
        element.name = "a"
        element.description = "b"

        element_dto = ElementDto(element)

        self.assertEqual("a", element_dto.name)
        self.assertEqual("b", element_dto.description)

    def test_elementVersioned(self):
        element = Element
        element.name = "a"
        element.description = "b"

        element_dto = ElementVersionedDto(element)

        self.assertEqual("a", element_dto.name)
        self.assertEqual([], element_dto.description)

    def test_version(self):
        version = Version
        version.name = "a"
        version.description = "b"
        version.uri = "c"
        version.major = 2
        version.minor = 3
        version.status = Version.Status.draft

        version_dto = VersionDto(version)

        self.assertEqual("a", version_dto.name)
        self.assertEqual("b", version_dto.description)
        self.assertEqual("c", version_dto.uri)
        self.assertEqual(2, version_dto.major)
        self.assertEqual(3, version_dto.minor)

    def test_version_compare__with_major(self):
        version1 = VersionDto(Version())
        version2 = VersionDto(Version())
        version1.major = 1
        version2.major = 2

        self.assertEqual(version1, sorted([version2, version1])[0])

    def test_version_compare__with_minor(self):
        version1 = VersionDto(Version())
        version2 = VersionDto(Version())
        version1.major = 1
        version1.minor = 1
        version2.major = 1
        version2.minor = 2

        self.assertEqual(version1, sorted([version2, version1])[0])

    def test_version_compare__with_name(self):
        version1 = VersionDto(Version())
        version2 = VersionDto(Version())
        version1.major = 1
        version1.minor = 1
        version1.name = "a"
        version2.major = 1
        version2.minor = 1
        version2.name = "b"

        self.assertEqual(version1, sorted([version2, version1])[0])

    def test_category(self):
        category = Category("a")
        category.name = "a"
        category.description = "b"
        category.order = 2

        category_dto = CategoryDto(category)

        self.assertEqual("a", category_dto.name)
        self.assertEqual("b", category_dto.description)
        self.assertEqual(2, category_dto.order)

    def test_category_compare__with_order(self):
        category1 = CategoryDto(Category("c"))
        category2 = CategoryDto(Category("c"))
        category1.order = 1
        category2.order = 2

        self.assertEqual(category1, sorted([category2, category1])[0])

    def test_category_compare__with_name(self):
        category1 = CategoryDto(Category("a"))
        category2 = CategoryDto(Category("b"))
        category1.order = 1
        category2.order = 1

        self.assertEqual(category1, sorted([category2, category1])[0])

    def test_typeCategory(self):
        category = Category("a")
        category.name = "a"
        category.description = "b"
        category.order = 2

        category_dto = TypeCategoryDto(category)

        self.assertEqual("a", category_dto.name)
        self.assertEqual("b", category_dto.description)
        self.assertEqual(2, category_dto.order)
        self.assertEqual([], category_dto.types)

    def test_methodCategory(self):
        category = Category("a")
        category.name = "a"
        category.description = "b"
        category.order = 2

        category_dto = MethodCategoryDto(category)

        self.assertEqual("a", category_dto.name)
        self.assertEqual("b", category_dto.description)
        self.assertEqual(2, category_dto.order)
        self.assertEqual([], category_dto.methods)

    def test_method(self):
        method = Method()
        method.name = "a"
        method.description = "b"
        method.method = Method.Methods.put

        method_dto = MethodDto(method)

        self.assertEqual("a", method_dto.name)
        self.assertEqual("put", str(method_dto.method))
        self.assertEqual([], method_dto.description)

        self.assertEqual([], method_dto.code)
        self.assertEqual([], method_dto.full_uri)
        self.assertEqual([], method_dto.absolute_uri)
        self.assertEqual([], method_dto.request_headers)
        self.assertEqual([], method_dto.request_parameters)
        self.assertEqual([], method_dto.request_body)
        self.assertEqual([], method_dto.response_codes)
        self.assertEqual([], method_dto.response_body)
        self.assertEqual([], method_dto.versions)
        self.assertEqual({}, method_dto.changes_status)
        self.assertEqual({}, method_dto.samples)

    def test_method_compare__with_name(self):
        method1 = MethodDto(Method())
        method2 = MethodDto(Method())

        method1.name = "a"
        method2.name = "b"

        self.assertEqual(method1, sorted([method2, method1])[0])

    def test_multiVersion(self):
        multi_version_dto = MultiVersionDto("a", "b")

        self.assertEqual("a", multi_version_dto.value)
        self.assertEqual(["b"], multi_version_dto.versions)

    def test_multiVersion_compare__with_name(self):
        multi_version1 = MultiVersionDto("a", "b")
        multi_version2 = MultiVersionDto("b", "b")

        self.assertEqual(multi_version1, sorted([multi_version2, multi_version1])[0])

    def test_multiVersion_compare__with_version(self):
        multi_version1 = MultiVersionDto("a", "b")
        multi_version2 = MultiVersionDto("a", "c")

        self.assertEqual(multi_version1, sorted([multi_version2, multi_version1])[0])

    def test_parameter(self):
        parameter = Parameter()
        parameter.name = "a"
        parameter.description = "b"
        parameter.type = "foo"
        parameter.optional = False

        parameter_dto = ParameterDto(parameter)

        self.assertEqual("a", parameter_dto.name)
        self.assertEqual("b", parameter_dto.description)
        self.assertEqual(False, parameter_dto.optional)
        self.assertEqual(False, parameter_dto.is_internal)

    def test_parameter_compare__with_name(self):
        parameter1 = ParameterDto(Parameter())
        parameter2 = ParameterDto(Parameter())
        parameter1.name = "a"
        parameter2.name = "b"

        self.assertEqual(parameter1, sorted([parameter2, parameter1])[0])

    def test_parameter_compare__with_description(self):
        parameter1 = ParameterDto(Parameter())
        parameter2 = ParameterDto(Parameter())
        parameter1.name = "a"
        parameter1.description = "a"
        parameter2.name = "a"
        parameter2.description = "b"

        self.assertEqual(parameter1, sorted([parameter2, parameter1])[0])

    def test_positionable_parameter(self):
        parameter = Parameter()
        parameter.name = "a"
        parameter.description = "b"
        parameter.type = "foo"
        parameter.optional = False

        parameter_dto = PositionableParameterDto(parameter)

        self.assertEqual("a", parameter_dto.name)
        self.assertEqual("b", parameter_dto.description)
        self.assertEqual(False, parameter_dto.optional)
        self.assertEqual(False, parameter_dto.is_internal)
        self.assertEqual(0, parameter_dto.position)

    def test_positionable_parameter_compare__with_position(self):
        parameter1 = PositionableParameterDto(Parameter())
        parameter2 = PositionableParameterDto(Parameter())
        parameter1.position = 1
        parameter2.position = 2

        self.assertTrue(parameter1 < parameter2)
        self.assertEqual(parameter1, parameter2)

    def test_response_code(self):
        parameter = ResponseCode()
        parameter.name = "a"
        parameter.description = "b"
        parameter.code = 300
        parameter.message = "c"

        parameter_dto = ResponseCodeDto(parameter)

        self.assertEqual("a", parameter_dto.name)
        self.assertEqual("b", parameter_dto.description)
        self.assertEqual(300, parameter_dto.code)
        self.assertEqual("c", parameter_dto.message)

    def test_response_code_compare__with_code(self):
        response_code1 = ResponseCodeDto(ResponseCode())
        response_code2 = ResponseCodeDto(ResponseCode())
        response_code1.code = 1
        response_code2.code = 2

        self.assertEqual(response_code1, sorted([response_code2, response_code1])[0])

    def test_response_code_compare__with_message(self):
        response_code1 = ResponseCodeDto(ResponseCode())
        response_code2 = ResponseCodeDto(ResponseCode())
        response_code1.code = 1
        response_code1.message = "a"
        response_code2.code = 1
        response_code2.message = "b"

        self.assertEqual(response_code1, sorted([response_code2, response_code1])[0])

    def test_response_code_compare__with_description(self):
        response_code1 = ResponseCodeDto(ResponseCode())
        response_code2 = ResponseCodeDto(ResponseCode())
        response_code1.code = 1
        response_code1.message = "a"
        response_code1.description = "a"
        response_code2.code = 1
        response_code2.message = "a"
        response_code2.description = "b"

        self.assertEqual(response_code1, sorted([response_code2, response_code1])[0])

    def test_type(self):
        type = Type()
        type.name = "a"
        type.description = "b"

        type_dto = TypeDto(type)

        self.assertEqual("a", type_dto.name)
        self.assertEqual([], type_dto.description)
        self.assertIsInstance(type_dto.format, TypeFormatDto)

        self.assertEqual([], type_dto.primary)
        self.assertEqual([], type_dto.values)
        self.assertEqual([], type_dto.versions)
        self.assertEqual({}, type_dto.changes_status)
        self.assertEqual({}, type_dto.samples)

    def test_type_compare__with_name(self):
        type1 = TypeDto(Type())
        type2 = TypeDto(Type())

        type1.name = "a"
        type2.name = "b"

        self.assertEqual(type1, sorted([type2, type1])[0])

    def test_typeFormat(self):
        type_format = TypeFormat()
        type_format.sample = "a"
        type_format.pretty = "b"

        type_format_dto = TypeFormatDto(type_format)

        self.assertEqual([], type_format_dto.sample)
        self.assertEqual([], type_format_dto.pretty)
        self.assertEqual([], type_format_dto.advanced)

    def test_typeValue(self):
        type = EnumTypeValue()
        type.name = "a"
        type.description = "b"

        type_value_dto = EnumTypeValueDto(type)

        self.assertEqual("a", type_value_dto.name)
        self.assertEqual("b", type_value_dto.description)

    def test_typeValue_compare__with_name(self):
        type_value1 = EnumTypeValueDto(EnumTypeValue())
        type_value2 = EnumTypeValueDto(EnumTypeValue())

        type_value1.name = "a"
        type_value2.name = "b"

        self.assertEqual(type_value1, sorted([type_value2, type_value1])[0])

    def test_typeValue_compare__with_description(self):
        type_value1 = EnumTypeValueDto(EnumTypeValue())
        type_value2 = EnumTypeValueDto(EnumTypeValue())

        type_value1.name = "a"
        type_value1.description = "a"
        type_value2.name = "a"
        type_value2.description = "b"

        self.assertEqual(type_value1, sorted([type_value2, type_value1])[0])

    def test_object_factory(self):
        self.assertIsInstance(ObjectDto.factory(Object.factory("object", "v1")), ObjectObjectDto)
        self.assertIsInstance(ObjectDto.factory(Object.factory("array", "v1")), ObjectArrayDto)
        self.assertIsInstance(ObjectDto.factory(Object.factory("number", "v1")), ObjectDto)
        self.assertIsInstance(ObjectDto.factory(Object.factory("string", "v1")), ObjectDto)
        self.assertIsInstance(ObjectDto.factory(Object.factory("bool", "v1")), ObjectDto)
        self.assertIsInstance(ObjectDto.factory(Object.factory("type", "v1")), ObjectTypeDto)
        self.assertIsInstance(ObjectDto.factory(Object.factory("none", "v1")), ObjectDto)
        self.assertIsInstance(ObjectDto.factory(Object.factory("dynamic", "v1")), ObjectDynamicDto)
        self.assertIsInstance(ObjectDto.factory(Object.factory("const", "v1")), ObjectConstDto)

    def test_object_compare__with_name(self):
        object1 = ObjectDto(Object())
        object2 = ObjectDto(Object())

        object1.name = "a"
        object2.name = "b"

        self.assertEqual(object1, sorted([object2, object1])[0])

    def test_object_compare__with_description(self):
        object1 = ObjectDto(Object())
        object2 = ObjectDto(Object())

        object1.name = "a"
        object1.description = "a"
        object2.name = "a"
        object2.description = "b"

        self.assertEqual(object1, sorted([object2, object1])[0])

    def test_object_compare__with_type(self):
        object1 = ObjectDto(Object())
        object2 = ObjectDto(Object())

        object1.name = "a"
        object1.description = "a"
        object1.type = Object.Types.bool
        object2.name = "a"
        object2.description = "a"
        object2.type = Object.Types.string

        self.assertEqual(object1, sorted([object2, object1])[0])

    def test_object_compare__with_optional(self):
        object1 = ObjectDto(Object())
        object2 = ObjectDto(Object())

        object1.name = "a"
        object1.description = "a"
        object1.type = Object.Types.bool
        object1.optional = False
        object2.name = "a"
        object2.description = "a"
        object2.type = Object.Types.bool
        object2.optional = True

        self.assertEqual(object1, sorted([object2, object1])[0])

    def test_object_compare__with_required(self):
        object1 = ObjectDto(Object())
        object2 = ObjectDto(Object())

        object1.name = "a"
        object1.description = "a"
        object1.type = Object.Types.bool
        object1.optional = True
        object1.required = False
        object2.name = "a"
        object2.description = "a"
        object2.type = Object.Types.bool
        object2.optional = True
        object2.required = True

        self.assertEqual(object1, sorted([object2, object1])[0])

    def test_objectObject(self):
        object_dto = ObjectObjectDto(Object())

        self.assertEqual({}, object_dto.properties)

    def test_objectArray(self):
        object_dto = ObjectArrayDto(Object())

        self.assertEqual(None, object_dto.items)

    def test_objectDynamic(self):
        object_dto = ObjectDynamicDto(Object())

        self.assertEqual(None, object_dto.items)

    def test_objectConst(self):
        object = ObjectConst()
        object.const_type = ObjectConst.Types.number
        object_dto = ObjectConstDto(object)

        self.assertEqual(ObjectConst.Types.number, object_dto.const_type)
        self.assertEqual(None, object_dto.value)

    def test_objectType(self):
        object = ObjectType()
        object.type_name = "a"
        object.primarie = "b"
        object.values = ["c"]

        object_dto = ObjectTypeDto(object)

        self.assertEqual("a", object_dto.type_name)
        self.assertEqual(None, object_dto.primary)
        self.assertEqual([], object_dto.values)
