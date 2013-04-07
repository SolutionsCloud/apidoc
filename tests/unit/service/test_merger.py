import unittest

from apidoc.service.merger import Merger


class TestParser(unittest.TestCase):

    def setUp(self):
        self.merger = Merger()

    def test_merge_sources_simple(self):
        self.assertEqual({"foo": "bar"}, self.merger.merge_sources([{"foo": "bar"}]))

    def test_merge_sources_with_none(self):
        self.assertEqual({"foo": "bar"}, self.merger.merge_sources([{"foo": "bar"}, None]))

    def test_merge_sources_with_complexe(self):
        datas = [
            {
                "a": {
                    "b": "foo"
                },
                "d": {
                    "e": [
                        "baz",
                        "qux"
                    ]
                }
            },
            {
                "a": {
                    "c": "bar"
                },
                "d": {
                    "e": [
                        "fum"
                    ]
                }
            }
        ]
        expected = {
            "a": {
                "b": "foo",
                "c": "bar"
            },
            "d": {
                "e": [
                    "baz",
                    "qux",
                    "fum"
                ]
            }
        }
        self.assertEqual(expected, self.merger.merge_sources(datas))

    def test_merge_sources__failed_missing_datas(self):
        with self.assertRaises(ValueError):
            self.merger.merge_sources([])

    def test_merge_sources__failed_dict_to_list(self):
        with self.assertRaises(TypeError):
            self.merger.merge_sources([{"a": {}}, {"a": {}}, {"a": []}])

    def test_merge_sources__failed_list_to_dict(self):
        with self.assertRaises(TypeError):
            self.merger.merge_sources([{"a": []}, {"a": []}, {"a": {}}])

    def test_merge_sources__failed_string_to_dict(self):
        with self.assertRaises(TypeError):
            self.merger.merge_sources([{"a": "b"}, {"a": {}}])

    def test_merge_sources__failed_string_to_list(self):
        with self.assertRaises(TypeError):
            self.merger.merge_sources([{"a": "b"}, {"a": []}])

    def test_merge_sources__failed_conflict(self):
        with self.assertRaises(ValueError):
            self.merger.merge_sources([{"a": "b"}, {"a": "c"}])

    def test_merge_configs__failed_string_to_list(self):
        with self.assertRaises(TypeError):
            self.merger.merge_configs("a", [])

    def test_merge_configs__failed_dict_to_string(self):
        with self.assertRaises(TypeError):
            self.merger.merge_configs({}, [{}, "b"])

    def test_merge_configs__failed_dict_to_list(self):
        with self.assertRaises(TypeError):
            self.merger.merge_configs({}, [{}, []])

    def test_merge_configs(self):
        first = {
            "a": {
                "b": "0",
                "c": 1
            },
            "d": None
        }
        others = [
            {
                "a": {
                    "b": "second",
                    "c": 2
                },
                "e": "test"
            },
            {
                "a": {
                    "b": "third",
                },
            }
        ]
        response = self.merger.merge_configs(first, others)
        self.assertEqual("third", response["a"]["b"])
        self.assertEqual(2, response["a"]["c"])
        self.assertEqual(None, response["d"])
        self.assertIn("d", response)
        self.assertNotIn("e", response)
