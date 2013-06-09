import unittest

from apidoc.object.source_dto import Comparable
from apidoc.object.source_dto import Category as CategoryDto
from apidoc.object.source_raw import Category
from apidoc.object.source_dto import Version as VersionDto
from apidoc.object.source_raw import Version
from apidoc.object.source_dto import Parameter as ParameterDto
from apidoc.object.source_raw import Parameter
from apidoc.object.source_dto import Object as ObjectDto
from apidoc.object.source_raw import Object
from apidoc.object.source_dto import ResponseCode as ResponseCodeDto
from apidoc.object.source_raw import ResponseCode
from apidoc.object.source_dto import ObjectObject as ObjectObjectDto
from apidoc.object.source_dto import ObjectArray as ObjectArrayDto
from apidoc.object.source_dto import ObjectType as ObjectTypeDto
from apidoc.object.source_dto import ObjectDynamic as ObjectDynamicDto


class TestSource(unittest.TestCase):

    def test_comparable_equality__with_one_property(self):
        class C1(Comparable):
            def __init__(self, name):
                self.name = name

            def get_comparable_values_for_equality(self):
                return (self.name)

        comparable1 = C1("a")
        comparable2 = C1("a")
        comparable3 = C1("b")

        self.assertEqual(comparable1, comparable2)
        self.assertNotEqual(comparable1, comparable3)
        #self.assertEqual(comparable1, sorted([comparable2, comparable1])[0])

    def test_comparable_equality__with_multiple_property(self):
        class C1(Comparable):
            def __init__(self, name, description):
                self.name = name
                self.description = description

            def get_comparable_values_for_equality(self):
                return (self.name, self.description)

        comparable1 = C1("a", "b")
        comparable2 = C1("a", "b")
        comparable3 = C1("a", "c")

        self.assertEqual(comparable1, comparable2)
        self.assertNotEqual(comparable1, comparable3)

    def test_comparable_ordering__with_one_property(self):
        class C1(Comparable):
            def __init__(self, name):
                self.name = name

            def get_comparable_values_for_ordering(self):
                return (self.name)

        comparable1 = C1("a")
        comparable2 = C1("c")
        comparable3 = C1("b")

        self.assertEqual([comparable1, comparable3, comparable2], sorted([comparable1, comparable2, comparable3]))

    def test_comparable_ordering__with_multiple_property(self):
        class C1(Comparable):
            def __init__(self, name, description):
                self.name = name
                self.description = description

            def get_comparable_values_for_ordering(self):
                return (self.name, self.description)

        comparable1 = C1("a", "b")
        comparable2 = C1("b", "a")
        comparable3 = C1("a", "c")

        self.assertEqual([comparable1, comparable3, comparable2], sorted([comparable1, comparable2, comparable3]))

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

    def test_parameter_compare__with_position(self):
        parameter1 = ParameterDto(Parameter())
        parameter2 = ParameterDto(Parameter())
        parameter1.position = 1
        parameter2.position = 2

        self.assertEqual(parameter1, sorted([parameter2, parameter1])[0])

    def test_parameter_compare__with_name(self):
        parameter1 = ParameterDto(Parameter())
        parameter2 = ParameterDto(Parameter())
        parameter1.position = 1
        parameter1.name = "a"
        parameter2.position = 1
        parameter2.name = "b"

        self.assertEqual(parameter1, sorted([parameter2, parameter1])[0])

    def test_parameter_compare__with_description(self):
        parameter1 = ParameterDto(Parameter())
        parameter2 = ParameterDto(Parameter())
        parameter1.position = 1
        parameter1.name = "a"
        parameter1.description = "a"
        parameter2.position = 1
        parameter2.name = "a"
        parameter2.description = "b"

        self.assertEqual(parameter1, sorted([parameter2, parameter1])[0])

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

    def test_object_factory(self):
        self.assertIsInstance(ObjectDto.factory(Object.factory("object", "v1")), ObjectObjectDto)
        self.assertIsInstance(ObjectDto.factory(Object.factory("array", "v1")), ObjectArrayDto)
        self.assertIsInstance(ObjectDto.factory(Object.factory("number", "v1")), ObjectDto)
        self.assertIsInstance(ObjectDto.factory(Object.factory("string", "v1")), ObjectDto)
        self.assertIsInstance(ObjectDto.factory(Object.factory("bool", "v1")), ObjectDto)
        self.assertIsInstance(ObjectDto.factory(Object.factory("type", "v1")), ObjectTypeDto)
        self.assertIsInstance(ObjectDto.factory(Object.factory("none", "v1")), ObjectDto)
        self.assertIsInstance(ObjectDto.factory(Object.factory("dynamic", "v1")), ObjectDynamicDto)

    def test_object_factory_link(self):
        response = ObjectDto.factory(Object.factory("foo", "v1"))

        self.assertIsInstance(response, ObjectTypeDto)
        self.assertEqual("foo", response.type_name)
