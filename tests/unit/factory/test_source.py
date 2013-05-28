import unittest

from mock import patch, call
from apidoc.factory.source import Source as SourceFactory
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

    @patch.object(Parser, "load_from_file", side_effect=[{"e": "f"}, {"g": "h"}])
    @patch.object(Parser, "load_all_from_directory", side_effect=[[{"a": "b"}, {"c": "d"}], [{"z": "y"}]])
    @patch.object(Merger, "merge_sources", return_value={"i": "j"})
    @patch.object(Extender, "extends", return_value={"k": "l"})
    @patch.object(SourceFactory, "populate", return_value="populated")
    @patch.object(SourceFactory, "fix_versions", return_value=None)
    @patch.object(SourceFactory, "apply_config_filter", return_value=None)
    @patch.object(SourceFactory, "remove_undisplayed", return_value=None)
    @patch.object(SourceFactory, "refactor_hierarchy", return_value=None)
    @patch.object(SourceFactory, "get_extender_paths", return_value=["m", "n"])
    def test_create_from_config(self, mock_source_extender, mock_refactor, mock_undisplayed, mock_filter, mock_fix, mock_source, mock_extender, mock_merger, mock_parser_directory, mock_parser_file):
        config = ConfigObject()
        config["input"]["directories"] = ["directory1", "directory2"]
        config["input"]["files"] = ["file1", "file2"]
        config["input"]["arguments"] = {"var": "value"}

        response = self.source.create_from_config(config)

        self.assertEqual("populated", response)

        mock_source.assert_called_once_with({"k": "l"})
        mock_refactor.assert_called_once_with("populated")
        mock_fix.assert_called_once_with("populated")
        mock_undisplayed.assert_called_once_with("populated")
        mock_filter.assert_called_once_with("populated", config["filter"])
        mock_extender.assert_called_once_with({"i": "j"}, paths=["m", "n"], separator="/", extends_key='extends', inherit_key='inherit', removed_key='removed')
        mock_merger.assert_called_once_with([{"a": "b"}, {"c": "d"}, {"z": "y"}, {"e": "f"}, {"g": "h"}])
        mock_parser_directory.assert_has_calls([call('directory1'), call('directory2')])
        mock_parser_file.assert_has_calls([call('file1'), call('file2')])

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


    def test_apply_config_filter_version(self):
        root = Root()
        version1 = Version()
        version2 = Version()
        version3 = Version()
        version1.name = "v1"
        version2.name = "v2"
        version3.name = "v3"

        root.versions = {"v1": version1, "v2": version2, "v3": version3}

        config = ConfigObject()
        self.source.apply_config_filter(root, config["filter"])

        self.assertTrue(version1.display)
        self.assertTrue(version2.display)
        self.assertTrue(version3.display)

    def test_apply_config_filter_version_include(self):
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
        self.source.apply_config_filter(root, config["filter"])

        self.assertTrue(version1.display)
        self.assertFalse(version2.display)
        self.assertTrue(version3.display)

    def test_apply_config_filter_version_exclude(self):
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
        self.source.apply_config_filter(root, config["filter"])

        self.assertFalse(version1.display)
        self.assertTrue(version2.display)
        self.assertFalse(version3.display)

    def test_apply_config_filter_category(self):
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
        self.source.apply_config_filter(root, config["filter"])

        self.assertTrue(category1.display)
        self.assertTrue(category2.display)
        self.assertTrue(category3.display)

    def test_apply_config_filter_category_include(self):
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
        self.source.apply_config_filter(root, config["filter"])

        self.assertTrue(category1.display)
        self.assertFalse(category2.display)
        self.assertTrue(category3.display)

    def test_apply_config_filter_category_exclude(self):
        root = Root()

        category1 = Category("c1")
        category2 = Category("c2")
        category3 = Category("c3")

        root.categories = {"c1": category1, "c2": category2, "c3": category3}

        config = ConfigObject()
        config["filter"]["categories"]["excludes"] = ["c1", "c3"]
        self.source.apply_config_filter(root, config["filter"])

        self.assertFalse(category1.display)
        self.assertTrue(category2.display)
        self.assertFalse(category3.display)

    def test_remove_undisplayed(self):
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

        self.source.remove_undisplayed(root)

        self.assertEqual(1, len(root.versions))
        self.assertEqual(version2, root.versions["v2"])
        self.assertEqual(1, len(root.versions["v2"].methods))
        self.assertEqual(method1, root.versions["v2"].methods["m1"])

    def test_fix_version(self):
        root = Root()
        version1 = Version()
        version2 = Version()

        method11 = Method()
        method12 = Method()
        method21 = Method()
        method22 = Method()

        type11 = Type()
        type12 = Type()
        type21 = Type()
        type22 = Type()

        reference11 = ObjectObject()
        reference12 = ObjectObject()
        reference21 = ObjectObject()
        reference22 = ObjectObject()

        root.versions = {"v1": version1, "v2": version2}

        version1.methods = {"m1": method11, "m2": method12}
        version2.methods = {"m1": method21, "m2": method22}
        version1.types = {"t1": type11, "t2": type12}
        version2.types = {"t1": type21, "t2": type22}
        version1.references = {"r1": reference11, "r2": reference12}
        version2.references = {"r1": reference21, "r2": reference22}

        self.source.fix_versions(root)
        self.assertEqual("v1", method11.version)
        self.assertEqual("v2", type21.version)
        self.assertEqual("v2", reference21.version)

    def test_refactor_hierarchy(self):
        root = Root()
        version1 = Version()
        version2 = Version()

        category1 = Category("c")
        category2 = Category("c")

        method11 = Method()
        method11.category = "n1"
        method12 = Method()
        method12.category = "n2"
        method21 = Method()
        method21.category = "default"
        method22 = Method()
        method22.category = "default"

        type11 = Type()
        type11.category = "n1"
        type12 = Type()
        type12.category = "n2"
        type21 = Type()
        type21.category = "default"
        type22 = Type()
        type22.category = "default"

        reference11 = ObjectObject()
        reference12 = ObjectObject()
        reference21 = ObjectObject()
        reference22 = ObjectObject()

        root.categories = {"n1": category1, "n2": category2}
        root.versions = {"v1": version1, "v2": version2}

        version1.methods = {"m1": method11, "m2": method12}
        version2.methods = {"m1": method21, "m2": method22}
        version1.types = {"t1": type11, "t2": type12}
        version2.types = {"t1": type21, "t2": type22}
        version1.references = {"r1": reference11, "r2": reference12}
        version2.references = {"r1": reference21, "r2": reference22}

        self.source.refactor_hierarchy(root)

        self.assertEqual(2, len(root.methods))
        self.assertEqual(2, len(root.methods["m1"].versions))
        self.assertEqual(method12, root.methods["m2"].versions["v1"])

        self.assertEqual(3, len(root.method_categories))
        self.assertEqual(2, len(root.method_categories["default"].methods))
        self.assertEqual(method21, root.method_categories["default"].methods["m1"].versions["v2"])

        self.assertEqual(2, len(root.types))
        self.assertEqual(2, len(root.types["t1"].versions))
        self.assertEqual(type12, root.types["t2"].versions["v1"])

        self.assertEqual(2, len(root.references))
        self.assertEqual(2, len(root.references["r1"].versions))
        self.assertEqual(reference21, root.references["r1"].versions["v2"])

        self.assertEqual(3, len(root.type_categories))
        self.assertEqual(2, len(root.type_categories["default"].types))
        self.assertEqual(type21, root.type_categories["default"].types["t1"].versions["v2"])

    def test_sort_version_equals(self):
        v1 = Version()
        v1.major = 1
        v1.minor = 2
        v2 = Version()
        v2.major = 1
        v2.minor = 2
        self.assertEqual(v1, v2)

    def test_sort_version_lt(self):
        v1 = Version()
        v1.major = 1
        v1.minor = 2
        v2 = Version()
        v2.major = 1
        v2.minor = 3
        self.assertLess(v1, v2)

    def test_sort_category_equals(self):
        v1 = Category("a")
        v1.order = 1
        v2 = Category("a")
        v2.order = 1
        self.assertEqual(v1, v2)

    def test_sort_category_lt(self):
        v1 = Category("a")
        v2 = Category("b")
        self.assertLess(v1, v2)

    def test_sort_category_lt__on_order(self):
        v1 = Category("a")
        v1.order = 1
        v2 = Category("a")
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

    def test_get_extender_paths(self):
        paths = self.source.get_extender_paths()
        self.assertEqual(5, len(paths))

    def test_populate_element__default(self):
        datas = {"description": "c", "sample": "foo"}
        element = Element()
        self.source.populate_element(element, "o_name", datas)

        self.assertEqual("o_name", element.name)
        self.assertEqual("c", element.description)
        self.assertNotIn("display", vars(element))
        self.assertNotIn("sample", vars(element))

    def test_populate_element__sampleable(self):
        datas = {"description": "c", "sample": {"foo": "bar"}}
        element = Sampleable()
        self.source.populate_element(element, "o_name", datas)

        self.assertEqual("{'foo': 'bar'}", element.sample)

    def test_populate_element__displayable(self):
        datas = {"description": "c", "display": "false"}
        element = Displayable()
        self.source.populate_element(element, "o_name", datas)

        self.assertEqual(False, element.display)

    def test_populate_element__displayable_default(self):
        datas = {"description": "c"}
        element = Displayable()
        self.source.populate_element(element, "o_name", datas)

        self.assertEqual(True, element.display)

    def test_populate(self):
        datas = {"versions": {"v1": {}, "v2": {}}, "configuration": {"title": "foo"}, "categories": {"c1": {}}}
        response = self.source.populate(datas)

        self.assertIsInstance(response, Root)
        self.assertEqual(2, len(response.versions))
        self.assertIn("v1", response.versions)
        self.assertIsInstance(response.versions["v1"], Version)
        self.assertIn("v2", response.versions)
        self.assertEqual("v2", response.versions["v2"].name)
        self.assertIsInstance(response.configuration, Configuration)
        self.assertEqual("foo", response.configuration.title)
        self.assertEqual(1, len(response.categories))
        self.assertIn("c1", response.categories)
        self.assertIsInstance(response.categories["c1"], Category)

    def test_populate_configuration(self):
        datas = {"title": "foo", "description": "bar", "uri": "baz"}
        response = self.source.populate_configuration(datas)

        self.assertIsInstance(response, Configuration)
        self.assertEqual("foo", response.title)
        self.assertEqual("bar", response.description)
        self.assertEqual("baz", response.uri)

    def test_populate_version(self):
        datas = {
            "uri": "a", "major": 1, "minor": 2, "status": "beta",
            "description": "c",
            "extends": ["v1", "v2"],
            "methods": {"m_name": {"uri": "/"}},
            "references": {"r_name": {"type": "string"}},
            "types": {"t_name": {"primary": "string"}}
        }
        response = self.source.populate_version("o_name", datas)

        self.assertIsInstance(response, Version)
        self.assertEqual("a", response.uri)
        self.assertEqual(1, response.major)
        self.assertEqual(2, response.minor)
        self.assertIsInstance(response.status, Version.Status)
        self.assertEqual("beta", str(response.status))
        self.assertEqual("o_name", response.name)
        self.assertEqual("c", response.description)
        self.assertIn("m_name", response.methods)
        self.assertIsInstance(response.methods["m_name"], Method)
        self.assertEqual("m_name", response.methods["m_name"].name)
        self.assertIn("r_name", response.references)
        self.assertIsInstance(response.references["r_name"], ObjectString)
        self.assertEqual("r_name", response.references["r_name"].name)
        self.assertIn("t_name", response.types)
        self.assertIsInstance(response.types["t_name"], Type)
        self.assertEqual("t_name", response.types["t_name"].name)

    def test_populate_version__failed_wrong_status(self):
        with self.assertRaises(ValueError):
            self.source.populate_version("o_name", {"status": "foo"})

    def test_populate_category(self):
        datas = {
            "description": "c",
            "order": "10"
        }
        response = self.source.populate_category("o_name", datas)

        self.assertIsInstance(response, Category)
        self.assertEqual("o_name", response.name)
        self.assertEqual("c", response.description)

    def test_populate_method(self):
        datas = {
            "description": "c",
            "code": "302",
            "category": "y",
            "uri": "a",
            "method": "put",
            "request_headers": {"h_name": {}},
            "request_parameters": {"p_name": {}},
            "response_codes": [{"code": "302"}],
            "request_body": {"type": "string"},
            "response_body": {"type": "number"}
        }
        response = self.source.populate_method("o_name", datas)

        self.assertIsInstance(response, Method)
        self.assertEqual("o_name", response.name)
        self.assertEqual("y", response.category)
        self.assertEqual("c", response.description)
        self.assertEqual(302, response.code)
        self.assertEqual("a", response.uri)
        self.assertIsInstance(response.method, Method.Methods)
        self.assertEqual("put", str(response.method))
        self.assertIn("h_name", response.request_headers)
        self.assertIsInstance(response.request_headers["h_name"], Parameter)
        self.assertEqual("h_name", response.request_headers["h_name"].name)
        self.assertIn("p_name", response.request_parameters)
        self.assertIsInstance(response.request_parameters["p_name"], Parameter)
        self.assertEqual("p_name", response.request_parameters["p_name"].name)
        self.assertIsInstance(response.request_body, ObjectString)
        self.assertIsInstance(response.response_codes, list)
        self.assertIsInstance(response.response_body, ObjectNumber)
        self.assertEqual(1, len(response.response_codes))

    def test_populate_method__failed_wrong_method(self):
        with self.assertRaises(ValueError):
            self.source.populate_method("o_name", {"method": "foo"})

    def test_populate_parameter(self):
        datas = {
            "description": "c",
            "type": "a",
            "sample": "b",
            "optional": "1"
        }
        response = self.source.populate_parameter("o_name", datas)

        self.assertIsInstance(response, Parameter)
        self.assertEqual("o_name", response.name)
        self.assertEqual("c", response.description)
        self.assertEqual("a", response.type)
        self.assertEqual("b", response.sample)
        self.assertEqual(True, response.optional)

    def test_populate_response_code(self):
        datas = {
            "code": 200,
            "description": "c",
            "message": "a",
        }
        response = self.source.populate_response_code(datas)

        self.assertIsInstance(response, ResponseCode)
        self.assertEqual("200", response.name)
        self.assertEqual("c", response.description)
        self.assertEqual(200, response.code)
        self.assertEqual("a", response.message)

    def test_populate_parameter__failed_missing_code(self):
        with self.assertRaises(ValueError):
            self.source.populate_response_code({})

    def test_populate_type(self):
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
        response = self.source.populate_type("o_name", datas)

        self.assertIsInstance(response, Type)
        self.assertEqual("o_name", response.name)
        self.assertEqual("c", response.description)
        self.assertIsInstance(response.primary, Type.Primaries)
        self.assertEqual("string", str(response.primary))
        self.assertIsInstance(response.format, TypeFormat)
        self.assertEqual("p", response.format.pretty)
        self.assertEqual("s", response.format.sample)
        self.assertEqual("d", response.format.advanced)

    def test_populate_type__failed_missing_primary(self):
        with self.assertRaises(ValueError):
            self.source.populate_type("o_name", {})

    def test_populate_typ__failed_wrong_primary(self):
        with self.assertRaises(ValueError):
            self.source.populate_type("o_name", {"primary": "foo"})

    def test_populate_type__enum(self):
        datas = {
            "primary": "enum",
            "values": {"a": {"description": "b"}}
        }
        response = self.source.populate_type("o_name", datas)

        self.assertIsInstance(response, EnumType)
        self.assertIsInstance(response.primary, Type.Primaries)
        self.assertEqual("enum", str(response.primary))
        self.assertIn("a", response.values)
        self.assertIsInstance(response.values["a"], EnumTypeValue)
        self.assertEqual("a", response.values["a"].name)

    def test_populate_type__enum__failed_missing_primary(self):
        with self.assertRaises(ValueError):
            self.source.populate_type("o_name", {})

    def test_populate_type__enum__failed_wrong_primary(self):
        with self.assertRaises(ValueError):
            self.source.populate_type("o_name", {"primary": "foo"})

    def test_populate_object(self):
        datas = {
            "description": "c",
            "type": "object",
            "properties": {
                "foo": {
                    "type": "string",
                    "description": "c_foo",
                    "optional": "true",
                    "required": "true",
                    "sample": "s_foo"
                },
                "bar": {
                    "type": "number",
                    "description": "c_bar",
                    "optional": "false",
                    "required": "false",
                    "sample": "123.4"
                },
                "baz": {
                    "type": "bool",
                    "description": "c_baz",
                    "sample": "true"
                },
                "qux": {
                    "type": "none",
                    "description": "c_qux"
                },
                "fum": {
                    "type": "reference",
                    "description": "c_fum",
                    "reference": "r_fum"
                },
                "foofoo": {
                    "type": "dynamic",
                    "description": "c_foofoo",
                    "items": "t_foofoo",
                    "sample": {
                        "a": "b",
                        "c": "d"
                    }
                },
                "foobar": {
                    "type": "t_foobar",
                    "description": "c_foobar",
                    "sample": "s_foobar"
                },
                "foobaz": {
                    "type": "array",
                    "description": "c_foobaz",
                    "sample_count": 2,
                    "items": {
                        "type": "object",
                        "properties": {
                            "fooqux": {
                                "type": "string"
                            }
                        }
                    }
                }
            }
        }

        response = self.source.populate_object("o_name", datas)

        self.assertIsInstance(response, ObjectObject)
        self.assertIsInstance(response.type, Object.Types)
        self.assertEqual("object", str(response.type))
        self.assertEqual("c", response.description)

        self.assertIn("foo", response.properties)
        self.assertIsInstance(response.properties["foo"], ObjectString)
        self.assertEqual("c_foo", response.properties["foo"].description)
        self.assertEqual("foo", response.properties["foo"].name)
        self.assertEqual("s_foo", response.properties["foo"].sample)
        self.assertEqual(True, response.properties["foo"].optional)
        self.assertEqual(True, response.properties["foo"].required)

        self.assertIn("bar", response.properties)
        self.assertIsInstance(response.properties["bar"], ObjectNumber)
        self.assertEqual("c_bar", response.properties["bar"].description)
        self.assertEqual("bar", response.properties["bar"].name)
        self.assertEqual("123.4", response.properties["bar"].sample)
        self.assertEqual(False, response.properties["bar"].optional)
        self.assertEqual(False, response.properties["bar"].required)

        self.assertIn("baz", response.properties)
        self.assertIsInstance(response.properties["baz"], ObjectBool)
        self.assertEqual("c_baz", response.properties["baz"].description)
        self.assertEqual("baz", response.properties["baz"].name)
        self.assertEqual(True, response.properties["baz"].sample)
        self.assertEqual(False, response.properties["baz"].optional)
        self.assertEqual(True, response.properties["baz"].required)

        self.assertIn("qux", response.properties)
        self.assertIsInstance(response.properties["qux"], ObjectNone)
        self.assertEqual("c_qux", response.properties["qux"].description)
        self.assertEqual("qux", response.properties["qux"].name)

        self.assertIn("fum", response.properties)
        self.assertIsInstance(response.properties["fum"], ObjectReference)
        self.assertEqual("c_fum", response.properties["fum"].description)
        self.assertEqual("fum", response.properties["fum"].name)
        self.assertEqual("r_fum", response.properties["fum"].reference_name)

        self.assertIn("foofoo", response.properties)
        self.assertIsInstance(response.properties["foofoo"], ObjectDynamic)
        self.assertEqual("c_foofoo", response.properties["foofoo"].description)
        self.assertEqual("foofoo", response.properties["foofoo"].name)
        self.assertEqual("t_foofoo", response.properties["foofoo"].items)
        self.assertEqual({"a": "b", "c": "d"}, response.properties["foofoo"].sample)

        self.assertIn("foobar", response.properties)
        self.assertIsInstance(response.properties["foobar"], ObjectType)
        self.assertEqual("c_foobar", response.properties["foobar"].description)
        self.assertEqual("foobar", response.properties["foobar"].name)
        self.assertEqual("t_foobar", response.properties["foobar"].type_name)
        self.assertEqual("s_foobar", response.properties["foobar"].sample)

        self.assertIn("foobaz", response.properties)
        self.assertIsInstance(response.properties["foobaz"], ObjectArray)
        self.assertEqual("c_foobaz", response.properties["foobaz"].description)
        self.assertEqual("foobaz", response.properties["foobaz"].name)
        self.assertEqual(2, response.properties["foobaz"].sample_count)
        self.assertIsInstance(response.properties["foobaz"].items, ObjectObject)
        self.assertEqual("items", response.properties["foobaz"].items.name)

    def test_populate_object__failed_missing_type(self):
        with self.assertRaises(ValueError):
            self.source.populate_object("o_name", {})

    def test_populate_object__failed_wrong_type(self):
        with self.assertRaises(ValueError):
            self.source.populate_object("o_name", {"type": "dynamic", "sample": []})
