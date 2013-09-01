import os
import unittest

from mock import patch, call
from apidoc.factory.source import Source as SourceFactory
from apidoc.object.config import Config as ConfigObject

from apidoc.object.source_raw import Root, Version, Category, Method, Type, Parameter, Object
from apidoc.object.source_raw import ObjectReference, ObjectObject, ObjectType, ObjectArray, ObjectDynamic, ObjectString
from apidoc.object.source_dto import Root as RootDto
from apidoc.object.source_dto import Category as CategoryDto

from apidoc.service.parser import Parser
from apidoc.service.merger import Merger
from apidoc.service.extender import Extender


class TestSource(unittest.TestCase):

    def setUp(self):
        self.source = SourceFactory()

    def test_parser(self):
        self.assertIsInstance(self.source.parser, Parser)

        self.source.parser = "foo"
        self.assertEqual("foo", self.source.parser)

        self.source.parser = None
        self.assertIsInstance(self.source.parser, Parser)

    def test_extender(self):
        self.assertIsInstance(self.source.extender, Extender)

        self.source.extender = "foo"
        self.assertEqual("foo", self.source.extender)

        self.source.extender = None
        self.assertIsInstance(self.source.extender, Extender)

    def test_merger(self):
        self.assertIsInstance(self.source.merger, Merger)

        self.source.merger = "foo"
        self.assertEqual("foo", self.source.merger)

        self.source.merger = None
        self.assertIsInstance(self.source.merger, Merger)

    @patch.object(Parser, "load_from_file", side_effect=[{"e": "f"}, {"g": "h"}, {}])
    @patch.object(Parser, "load_all_from_directory", side_effect=[[{"a": "b"}, {"c": "d"}], [{"z": "y"}]])
    @patch.object(Merger, "merge_sources", return_value={"i": "j"})
    @patch.object(Extender, "extends", return_value={})
    def test_create_from_config(self, mock_extender, mock_merger, mock_parser_directory, mock_parser_file):
        config = ConfigObject()
        init = os.path.isdir
        try:
            os.path.isdir = lambda x: x[0] == "d"
            config["input"]["locations"] = ["d1", "d2", "f1", "f2"]
            config["input"]["arguments"] = {"var": "value"}

            response = self.source.create_from_config(config)

            self.assertIsInstance(response, RootDto)

            mock_extender.assert_called_once_with({"i": "j"}, paths=('categories/?', 'versions/?', 'versions/?/methods/?', 'versions/?/types/?', 'versions/?/references/?'))
            mock_merger.assert_called_once_with([{"a": "b"}, {"c": "d"}, {"z": "y"}, {"e": "f"}, {"g": "h"}])
            mock_parser_directory.assert_has_calls([call("d1"), call("d2")])
            mock_parser_file.assert_has_calls([call("f1"), call("f2")])
        finally:
            os.path.isdir = init

    @patch.object(Parser, "load_from_file", side_effect=[{"e": "f"}, {"g": "h"}, {}])
    @patch.object(Parser, "load_all_from_directory", side_effect=[[{"a": "b"}, {"c": "d"}], [{"z": "y"}]])
    @patch.object(Merger, "merge_sources", return_value={"i": "j"})
    @patch.object(Extender, "extends", return_value={})
    def test_create_from_config__without_validation(self, mock_extender, mock_merger, mock_parser_directory, mock_parser_file):
        config = ConfigObject()
        init = os.path.isdir
        try:
            os.path.isdir = lambda x: x[0] == "d"

            config["input"]["locations"] = ["d1", "d2", "f1", "f2"]
            config["input"]["arguments"] = {"var": "value"}
            config["input"]["validate"] = False

            response = self.source.create_from_config(config)

            self.assertIsInstance(response, RootDto)

            mock_extender.assert_called_once_with({"i": "j"}, paths=('categories/?', 'versions/?', 'versions/?/methods/?', 'versions/?/types/?', 'versions/?/references/?'))
            mock_merger.assert_called_once_with([{"a": "b"}, {"c": "d"}, {"z": "y"}, {"e": "f"}, {"g": "h"}])
            mock_parser_directory.assert_has_calls([call("d1"), call("d2")])
            mock_parser_file.assert_has_calls([call("f1"), call("f2")])
        finally:
            os.path.isdir = init

    def test_get_sources_from_config(self):
        config = ConfigObject()

        response = self.source.get_sources_from_config(config)

        self.assertEqual([], response)

    def test_inject_arguments_in_sources(self):
        source = "foo"

        response = self.source.inject_arguments_in_sources(source, None)

        self.assertEqual("foo", response)

    def test_replace_argument(self):
        root = {
            "a": "${a1}",
            "b": [
                "c",
                "${a1}",
                {
                    "d": "${a1}",
                    "e": "f",
                    "g": 123,
                }
            ],
        }

        response = self.source.replace_argument(root, "a1", "v")
        self.assertEqual({
            "a": "v",
            "b": [
                "c",
                "v",
                {
                    "d": "v",
                    "e": "f",
                    "g": 123,
                }
            ],
        }, response)

    def test_hide_filtered_elements__version(self):
        root = Root()
        version1 = Version()
        version2 = Version()
        version3 = Version()
        version1.name = "v1"
        version2.name = "v2"
        version3.name = "v3"

        root.versions = {"v1": version1, "v2": version2, "v3": version3}

        config = ConfigObject()
        self.source.hide_filtered_elements(root, config["filter"])

        self.assertTrue(version1.display)
        self.assertTrue(version2.display)
        self.assertTrue(version3.display)

    def test_hide_filtered_elements__version_include(self):
        root = Root()
        version1 = Version()
        version2 = Version()
        version3 = Version()
        version1.name = "v1"
        version2.name = "v2"
        version3.name = "v3"

        root.versions = {"v1": version1, "v2": version2, "v3": version3}

        config = ConfigObject()
        config["filter"]["versions"]["includes"] = ["v1", "v3"]
        self.source.hide_filtered_elements(root, config["filter"])

        self.assertTrue(version1.display)
        self.assertFalse(version2.display)
        self.assertTrue(version3.display)

    def test_hide_filtered_elements__version_exclude(self):
        root = Root()
        version1 = Version()
        version2 = Version()
        version3 = Version()
        version1.name = "v1"
        version2.name = "v2"
        version3.name = "v3"

        root.versions = {"v1": version1, "v2": version2, "v3": version3}

        config = ConfigObject()
        config["filter"]["versions"]["excludes"] = ["v1", "v3"]
        self.source.hide_filtered_elements(root, config["filter"])

        self.assertFalse(version1.display)
        self.assertTrue(version2.display)
        self.assertFalse(version3.display)

    def test_hide_filtered_elements__category(self):
        root = Root()
        version1 = Version()

        category1 = Category("c")
        category2 = Category("c")
        category3 = Category("c")
        category1.name = "v1"
        category2.name = "v2"
        category3.name = "v3"

        root.versions = {"v1": version1}
        version1.categories = {"s1": category1, "s2": category2, "s3": category3}

        config = ConfigObject()
        self.source.hide_filtered_elements(root, config["filter"])

        self.assertTrue(category1.display)
        self.assertTrue(category2.display)
        self.assertTrue(category3.display)

    def test_hide_filtered_elements__category_include(self):
        root = Root()

        category1 = Category("c")
        category2 = Category("c")
        category3 = Category("c")
        category1.name = "v1"
        category2.name = "v2"
        category3.name = "v3"

        root.categories = {"s1": category1, "s2": category2, "s3": category3}

        config = ConfigObject()
        config["filter"]["categories"]["includes"] = ["v1", "v3"]
        self.source.hide_filtered_elements(root, config["filter"])

        self.assertTrue(category1.display)
        self.assertFalse(category2.display)
        self.assertTrue(category3.display)

    def test_hide_filtered_elements__category_exclude(self):
        root = Root()

        category1 = Category("c1")
        category2 = Category("c2")
        category3 = Category("c3")

        root.categories = {"c1": category1, "c2": category2, "c3": category3}

        config = ConfigObject()
        config["filter"]["categories"]["excludes"] = ["c1", "c3"]
        self.source.hide_filtered_elements(root, config["filter"])

        self.assertFalse(category1.display)
        self.assertTrue(category2.display)
        self.assertFalse(category3.display)

    def test_remove_unused_types(self):
        root = Root()

        version1 = Version()

        type1 = Type()
        type2 = Type()

        method1 = Method()

        parameter1 = Parameter()
        parameter1.type = "t1"

        method1.request_parameters = {"p1": parameter1}

        version1.types = {"t1": type1, "t2": type2}
        version1.methods = {"m1": method1}

        root.versions = {"v1": version1}

        self.source.remove_unused_types(root)

        self.assertEqual({"t1": type1}, version1.types)

    def test_replace_references(self):
        root = Root()

        version1 = Version()

        method1 = Method()
        type1 = Type()

        object_reference1 = ObjectReference()
        object_reference1.reference_name = "r1"
        object_reference1.name = "a"

        object_reference2 = ObjectReference()
        object_reference2.reference_name = "r1"
        object_reference2.name = "a"

        object1 = ObjectObject()
        object1.description = "b"

        method1.request_body = object_reference1
        type1.item = object_reference2

        version1.references = {"r1": object1}
        version1.methods = {"m1": method1}
        version1.types = {"t1": type1}

        root.versions = {"v1": version1}

        self.source.replace_references(root)

        self.assertEqual("a", method1.request_body.name)
        self.assertEqual("b", method1.request_body.description)
        self.assertEqual("a", type1.item.name)
        self.assertEqual("b", type1.item.description)

    def test_replace_type(self):
        root = Root()

        version1 = Version()

        method1 = Method()

        object_type1 = ObjectType()
        object_type1.type_name = "t1"

        type1 = Type()

        parameter1 = Parameter()
        parameter1.type = "t1"

        parameter2 = Parameter()
        parameter2.type = "t1"

        method1.request_body = object_type1
        method1.request_parameters = {"p1": parameter1}
        method1.request_headers = {"p1": parameter2}

        version1.types = {"t1": type1}
        version1.methods = {"m1": method1}

        root.versions = {"v1": version1}

        self.source.replace_types(root)

        self.assertEqual(type1, method1.request_body.type_object)
        self.assertEqual(type1, method1.request_parameters["p1"].type_object)
        self.assertEqual(type1, method1.request_headers["p1"].type_object)

    def test_replace_references_in_object(self):
        object = ObjectObject()
        array = ObjectArray()
        dynamic = ObjectDynamic()
        reference = ObjectReference()
        reference.reference_name = "r1"

        string1 = ObjectString()

        object.properties = {"p1": array}
        array.items = dynamic
        dynamic.items = reference

        self.source.replace_references_in_object(object, {"r1": string1})

        self.assertEqual(Object.Types.string, dynamic.items.type)

    def test_replace_types_in_object(self):
        object = ObjectObject()
        array = ObjectArray()
        dynamic = ObjectDynamic()
        reference = ObjectType()
        reference.type_name = "t1"

        type1 = Type()

        object.properties = {"p1": array}
        array.items = dynamic
        dynamic.items = reference

        self.source.replace_types_in_object(object, {"t1": type1})

        self.assertEqual(type1, reference.type_object)

    def test_replace_types_in_object_not_an_object(self):
        object = ObjectString()

        self.source.replace_types_in_object(object, {})

        self.assertEqual(vars(ObjectString()), vars(object))

    def test_replace_types_in_parameter___scalara(self):
        object = Parameter()
        object.type = "string"

        response = self.source.replace_types_in_parameter(object, {})

        self.assertEqual(object, response)

    def test_replace_types_in_object__unknwon(self):
        object = ObjectObject()
        array = ObjectArray()
        dynamic = ObjectDynamic()
        reference = ObjectType()
        reference.type_name = "t2"

        type1 = Type()

        object.properties = {"p1": array}
        array.items = dynamic
        dynamic.items = reference

        with self.assertRaises(ValueError):
            self.source.replace_types_in_object(object, {"t1": type1})

    def test_get_used_types_in_object(self):
        object = ObjectObject()
        array = ObjectArray()
        dynamic = ObjectDynamic()
        reference = ObjectType()
        reference.type_name = "t1"

        object.properties = {"p1": array}
        array.items = dynamic
        dynamic.items = reference

        response = self.source.get_used_types_in_object(object)

        self.assertEqual(["t1"], response)

    def test_get_used_types_in_object__for_scalara(self):
        object = ObjectString()

        response = self.source.get_used_types_in_object(object)

        self.assertEqual([], response)

    def test_get_reference(self):
        reference = ObjectReference()
        reference.reference_name = "r1"
        reference.name = "a"
        reference.description = "b"
        reference.optional = True

        reference1 = ObjectReference()
        reference1.reference_name = "r2"

        reference2 = ObjectString()

        response = self.source.get_reference(reference, {"r1": reference1, "r2": reference2})

        self.assertNotEqual(reference2, response)
        self.assertEqual("a", response.name)
        self.assertEqual("b", response.description)
        self.assertEqual(True, response.optional)

    def test_remove_hidden_elements(self):
        root = Root()
        version1 = Version()
        version2 = Version()
        category1 = Category("c1")
        category2 = Category("c2")
        method1 = Method()
        method2 = Method()

        root.versions = {"v1": version1, "v2": version2}
        root.categories = {"c1": category1, "c2": category2}

        version1.methods = {"m1": method1, "m2": method2}
        version2.methods = {"m1": method1, "m2": method2}

        method1.category = "c1"
        method2.category = "c2"

        version1.display = False
        category2.display = False

        self.source.remove_hidden_elements(root)

        self.assertEqual(1, len(root.versions))
        self.assertEqual(version2, root.versions["v2"])
        self.assertEqual(1, len(root.versions["v2"].methods))
        self.assertEqual(method1, root.versions["v2"].methods["m1"])

    def test_add_missing_categories(self):
        root = Root()
        version1 = Version()
        category1 = Category("c1")
        method1 = Method()
        method2 = Method()

        root.versions = {"v1": version1}
        root.categories = {"c1": category1}

        version1.methods = {"m1": method1, "m2": method2}

        method1.category = "c1"
        method2.category = "c2"

        self.source.add_missing_categories(root)

        self.assertEqual(2, len(root.categories))
        self.assertIsInstance(root.categories["c2"], Category)

    def test_sort_category_equals(self):
        v1 = CategoryDto(Category("a"))
        v1.order = 1
        v2 = CategoryDto(Category("a"))
        v2.order = 1
        self.assertEqual(v1, v2)

    def test_sort_category_lt(self):
        v1 = CategoryDto(Category("a"))
        v2 = CategoryDto(Category("b"))
        self.assertLess(v1, v2)

    def test_sort_category_lt__on_order(self):
        v1 = CategoryDto(Category("a"))
        v1.order = 1
        v2 = CategoryDto(Category("a"))
        v2.order = 2
        self.assertLess(v1, v2)

    def test_sort_method_equals(self):
        v1 = Method()
        v1.name = "a"
        v2 = Method()
        v2.name = "a"
        self.assertEqual(v1, v2)

    def test_sort_method_lt(self):
        v1 = Method()
        v1.name = "a"
        v2 = Method()
        v2.name = "b"
        self.assertLess(v1, v2)
