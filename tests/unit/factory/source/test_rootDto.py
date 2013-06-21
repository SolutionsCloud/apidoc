import unittest

from apidoc.factory.source.rootDto import RootDto as RootDtoFactory
from apidoc.factory.source.rootDto import Hydrator


#from apidoc.object.source_raw import Root, Element, Sampleable, Displayable
from apidoc.object.source_raw import Root, Version, Method, Type, Category, Parameter, EnumType
from apidoc.object.source_raw import ObjectString, ObjectArray, ObjectObject, ObjectDynamic, ObjectType, ObjectConst
from apidoc.object.source_dto import Root as RootDto
from apidoc.object.source_dto import Version as VersionDto
from apidoc.object.source_dto import MethodCategory, TypeCategory, MultiVersion, PositionableParameter
#from apidoc.object.source_raw import Version
#from apidoc.object.source_raw import Method, Category
#from apidoc.object.source_raw import Parameter, ResponseCode
#from apidoc.object.source_raw import Type, EnumType, EnumTypeValue, TypeFormat
#from apidoc.object.source_raw import Object, ObjectObject, ObjectArray
#from apidoc.object.source_raw import ObjectNumber, ObjectString, ObjectBool, ObjectNone
#from apidoc.object.source_raw import ObjectDynamic, ObjectReference, ObjectType


class TestRootDto(unittest.TestCase):

    def setUp(self):
        self.factory = RootDtoFactory()

    def test_create_from_root(self):
        root = Root()
        version = Version()
        version.name = "v"
        method = Method()
        method.category = "a"
        type = Type()
        type.category = "b"

        root.versions = {"v": version}
        version.methods = {"m": method}
        version.types = {"m": type}

        response = self.factory.create_from_root(root)

        self.assertIsInstance(response, RootDto)

        self.assertEqual(1, len(response.method_categories))
        self.assertEqual("a", response.method_categories[0].name)
        self.assertEqual(1, len(response.method_categories[0].methods))

        self.assertEqual(1, len(response.type_categories))
        self.assertEqual("b", response.type_categories[0].name)
        self.assertEqual(1, len(response.type_categories[0].types))

    def test_define_changes_status(self):
        root_dto = RootDto()

        version1 = Version()
        version1.name = "v1"
        version1.major = 1
        version1 = VersionDto(version1)
        version2 = Version()
        version2.name = "v2"
        version2.major = 2
        version2 = VersionDto(version2)

        category1 = MethodCategory(Category("c1"))
        category2 = TypeCategory(Category("c2"))

        method1 = Method()
        method1.changes_status = {"v1": MultiVersion.Changes.none}
        method2 = Method()
        method2.changes_status = {"v1": MultiVersion.Changes.new}
        method3 = Method()
        method3.changes_status = {"v2": MultiVersion.Changes.new}

        category1.methods = [method1, method2, method3]

        root_dto.versions = [version1, version2]
        root_dto.method_categories = [category1]
        root_dto.type_categories = [category2]

        self.factory.define_changes_status(root_dto)

        print(method1.changes_status)

        self.assertEqual(MultiVersion.Changes.new, method1.changes_status["v1"])
        self.assertEqual(MultiVersion.Changes.deleted, method2.changes_status["v2"])
        self.assertEqual(MultiVersion.Changes.none, method3.changes_status["v1"])


class TestHydrator(unittest.TestCase):

    def test_hydrate_method(self):

        root = Root()
        version = Version()
        version.name = "v"
        method = Method()
        method.category = "a"
        method.full_uri = "/{p}/"

        parameter = Parameter()
        parameter.name = "p"
        parameter.type = "string"
        method.request_parameters = {"p": parameter}

        root.versions = {"v": version}
        version.methods = {"m": method}
        version.types = {"m": type}

        root_dto = RootDto()

        hydrator = Hydrator(version, {"v": version}, [])

        hydrator.hydrate_method(root_dto, root, method)

        self.assertEqual(1, len(root_dto.method_categories))
        self.assertEqual(0, len(root_dto.type_categories))
        self.assertEqual(1, len(root_dto.method_categories[0].methods))
        self.assertEqual(1, len(root_dto.method_categories[0].methods[0].request_parameters))
        self.assertIsInstance(root_dto.method_categories[0].methods[0].request_parameters[0].value, PositionableParameter)
        self.assertEqual(1, root_dto.method_categories[0].methods[0].request_parameters[0].value.position)

    def test_hydrate_method__with_known_category(self):

        root = Root()
        version = Version()
        version.name = "v"
        method = Method()
        method.category = "c"

        root.versions = {"v": version}
        version.methods = {"m": method}
        version.types = {"m": type}

        category = Category("c")
        category.description = "d"

        root.categories = {"c": category}

        root_dto = RootDto()

        hydrator = Hydrator(version, {"v": version}, [])

        hydrator.hydrate_method(root_dto, root, method)

        self.assertEqual("d", root_dto.method_categories[0].description)

    def test_hydrate_method__with_multiple_methds(self):

        root = Root()
        version = Version()
        version.name = "v"
        method1 = Method()
        method1.category = "c"
        method2 = Method()
        method2.category = "c"

        root.versions = {"v": version}
        version.methods = {"m1": method1, "m2": method2}
        version.types = {"m": type}

        root_dto = RootDto()

        hydrator = Hydrator(version, {"v": version}, [])

        hydrator.hydrate_method(root_dto, root, method1)
        hydrator.hydrate_method(root_dto, root, method2)

        self.assertEqual(1, len(root_dto.method_categories))

    def test_hydrate_method_changed(self):

        root = Root()
        version1 = Version()
        version1.name = "v1"
        version2 = Version()
        version2.name = "v2"
        method1 = Method()
        method1.name = "m1"
        method1.description = "b"
        method2 = Method()
        method2.name = "m1"
        method2.description = "c"

        root.versions = {"v1": version1, "v2": version2}
        version1.methods = {"m1": method1}
        version2.methods = {"m1": method2}

        root_dto = RootDto()

        Hydrator(version1, root.versions, []).hydrate_method(root_dto, root, method1)
        Hydrator(version2, root.versions, []).hydrate_method(root_dto, root, method2)

        self.assertEqual(1, len(root_dto.method_categories))
        self.assertEqual(1, len(root_dto.method_categories[0].methods))
        self.assertEqual(2, len(root_dto.method_categories[0].methods[0].description))
        self.assertEqual(MultiVersion.Changes.updated, root_dto.method_categories[0].methods[0].changes_status["v2"])

    def test_hydrate_type(self):

        root = Root()
        version = Version()
        version.name = "v"
        type = EnumType()
        type.category = "a"
        type.full_uri = "/{p}/"

        parameter = Parameter()
        parameter.name = "p"
        parameter.type = "string"
        type.request_parameters = {"p": parameter}

        root.versions = {"v": version}
        version.types = {"m": type}
        version.types = {"m": type}

        root_dto = RootDto()

        hydrator = Hydrator(version, {"v": version}, [])

        hydrator.hydrate_type(root_dto, root, type)

        self.assertEqual(0, len(root_dto.method_categories))
        self.assertEqual(1, len(root_dto.type_categories))
        self.assertEqual(1, len(root_dto.type_categories[0].types))

    def test_hydrate_type__with_known_category(self):

        root = Root()
        version = Version()
        version.name = "v"
        type = Type()
        type.category = "c"

        root.versions = {"v": version}
        version.types = {"m": type}
        version.types = {"m": type}

        category = Category("c")
        category.description = "d"

        root.categories = {"c": category}

        root_dto = RootDto()

        hydrator = Hydrator(version, {"v": version}, [])

        hydrator.hydrate_type(root_dto, root, type)

        self.assertEqual("d", root_dto.type_categories[0].description)

    def test_hydrate_type__with_multiple_methds(self):

        root = Root()
        version = Version()
        version.name = "v"
        type1 = Type()
        type1.category = "c"
        type2 = Type()
        type2.category = "c"

        root.versions = {"v": version}
        version.types = {"m1": type1, "m2": type2}
        version.types = {"m": type}

        root_dto = RootDto()

        hydrator = Hydrator(version, {"v": version}, [])

        hydrator.hydrate_type(root_dto, root, type1)
        hydrator.hydrate_type(root_dto, root, type2)

        self.assertEqual(1, len(root_dto.type_categories))

    def test_hydrate_type_changed(self):

        root = Root()
        version1 = Version()
        version1.name = "v1"
        version2 = Version()
        version2.name = "v2"
        type1 = Type()
        type1.name = "m1"
        type1.description = "b"
        type2 = Type()
        type2.name = "m1"
        type2.description = "c"

        root.versions = {"v1": version1, "v2": version2}
        version1.types = {"m1": type1}
        version2.types = {"m1": type2}

        root_dto = RootDto()

        Hydrator(version1, root.versions, []).hydrate_type(root_dto, root, type1)
        Hydrator(version2, root.versions, []).hydrate_type(root_dto, root, type2)

        self.assertEqual(1, len(root_dto.type_categories))
        self.assertEqual(1, len(root_dto.type_categories[0].types))
        self.assertEqual(2, len(root_dto.type_categories[0].types[0].description))
        self.assertEqual(MultiVersion.Changes.updated, root_dto.type_categories[0].types[0].changes_status["v2"])

    def test_hydrate_value(self):

        version1 = Version()
        version1.name = "v1"
        version2 = Version()
        version2.name = "v2"

        versions = {"v1": version1, "v2": version2}

        object_dto = []
        object = "a"

        response = Hydrator(version1, versions, []).hydrate_value(object_dto, object)
        response = Hydrator(version2, versions, []).hydrate_value(object_dto, object)

        self.assertEqual(0, response)
        self.assertEqual(1, len(object_dto))
        self.assertEqual("a", object_dto[0].value)
        self.assertIn(version1.name, object_dto[0].versions)
        self.assertIn(version2.name, object_dto[0].versions)

    def test_hydrate_value__none(self):

        version1 = Version()
        version1.name = "v1"
        version2 = Version()
        version2.name = "v2"

        versions = {"v1": version1, "v2": version2}

        object_dto = []
        object = None

        response = Hydrator(version1, versions, []).hydrate_value(object_dto, object)

        self.assertEqual(0, response)
        self.assertEqual(0, len(object_dto))

    def test_hydrate_list(self):

        version1 = Version()
        version1.name = "v1"
        version2 = Version()
        version2.name = "v2"

        versions = {"v1": version1, "v2": version2}

        object_dto = []
        object = ["a", "b"]

        response = Hydrator(version1, versions, []).hydrate_list(object_dto, object)
        response = Hydrator(version2, versions, []).hydrate_list(object_dto, object)

        self.assertEqual(0, response)
        self.assertEqual(2, len(object_dto))
        self.assertEqual("a", object_dto[0].value)
        self.assertEqual("b", object_dto[1].value)
        self.assertIn(version1.name, object_dto[0].versions)
        self.assertIn(version2.name, object_dto[0].versions)

    def test_hydrate_object(self):

        version1 = Version()
        version1.name = "v1"
        version2 = Version()
        version2.name = "v2"

        versions = {"v1": version1, "v2": version2}

        object_dto = []

        object1 = ObjectObject()
        object2 = ObjectObject()
        object1.name = "a"
        object2.name = "a"
        array = ObjectArray()
        array.name = "b"
        dynamic = ObjectDynamic()
        dynamic.name = "c"
        string = ObjectString()
        string.name = "d"
        type = ObjectType()
        type.name = "e"
        type.items = "f"
        const = ObjectConst()
        const.value = "g"

        object1.properties = {"p1": array, "p3": const}
        object2.properties = {"p1": array, "p3": const, "p2": type}
        array.items = dynamic
        dynamic.items = string

        response = Hydrator(version1, versions, []).hydrate_object(object_dto, object1)
        response = Hydrator(version2, versions, []).hydrate_object(object_dto, object2)

        self.assertEqual(1, response)
        self.assertEqual(1, len(object_dto))
        self.assertIn(version1.name, object_dto[0].versions)
        self.assertIn(version2.name, object_dto[0].versions)
        self.assertEqual("a", object_dto[0].value.name)
        self.assertEqual("b", object_dto[0].value.properties["p1"][0].value.name)
        self.assertEqual("c", object_dto[0].value.properties["p1"][0].value.items[0].value.name)
        self.assertEqual("d", object_dto[0].value.properties["p1"][0].value.items[0].value.items[0].value.name)
        self.assertEqual("e", object_dto[0].value.properties["p2"][0].value.name)
        self.assertEqual("f", object_dto[0].value.properties["p2"][0].value.items)
        self.assertEqual("g", object_dto[0].value.properties["p3"][0].value.value)

    def test_get_previous_version__first(self):
        version1 = Version()
        version1.name = "v1"
        version1.major = 1
        version2 = Version()
        version2.name = "v2"
        version2.major = 2

        versions = {"v1": version1, "v2": version2}
        response = Hydrator(version1, versions, []).get_previous_version()

        self.assertEqual(None, response)

    def test_get_previous_version__second(self):
        version1 = Version()
        version1.name = "v1"
        version1.major = 1
        version2 = Version()
        version2.name = "v2"
        version2.major = 2

        versions = {"v1": version1, "v2": version2}
        response = Hydrator(version2, versions, []).get_previous_version()

        self.assertEqual(version1, response)

    def test_get_previous_version__unknown(self):
        version1 = Version()
        version1.name = "v1"
        version1.major = 1
        version2 = Version()
        version2.name = "v2"
        version2.major = 2
        version3 = Version()
        version3.name = "v3"
        version3.major = 3

        versions = {"v1": version1, "v2": version2}
        with self.assertRaises(ValueError):
            Hydrator(version3, versions, []).get_previous_version()
