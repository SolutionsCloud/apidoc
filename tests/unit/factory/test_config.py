import unittest
import os

from mock import patch

from apidoc.factory.config import Config as ConfigFactory
from apidoc.object.config import Config as ConfigObject
from apidoc.service.parser import Parser
from apidoc.service.merger import Merger


class TestConfig(unittest.TestCase):

    def setUp(self):
        self.config = ConfigFactory()

    def test_parser(self):
        self.assertIsInstance(self.config.parser, Parser)

        self.config.parser = "foo"
        self.assertEqual("foo", self.config.parser)

        self.config.parser = None
        self.assertIsInstance(self.config.parser, Parser)

    def test_merger(self):
        self.assertIsInstance(self.config.merger, Merger)

        self.config.merger = "foo"
        self.assertEqual("foo", self.config.merger)

        self.config.merger = None
        self.assertIsInstance(self.config.merger, Merger)

    @patch.object(Parser, "load_from_file", return_value={"output": {"location": "file2"}})
    def test_load_from_file(self, mock_parser):
        response = self.config.load_from_file("yaml_file")

        mock_parser.assert_called_once_with("yaml_file")

        self.assertIsInstance(response, ConfigObject)
        self.assertEqual(os.path.realpath("") + "/file2", response["output"]["location"])

    @patch.object(Parser, "load_from_file", return_value=None)
    def test_load_from_file__empty(self, mock_parser):
        response = self.config.load_from_file("yaml_file")

        mock_parser.assert_called_once_with("yaml_file")

        self.assertIsInstance(response, ConfigObject)
        self.assertEqual("stdout", response["output"]["location"])

    def test_fix_all_path(self):
        sample = {
            "input": {
                "directories": [
                    "directory",
                    "directory2/subdirectory"
                ],
                "files": [
                    "file",
                    "directory/file"
                ]
            },
            "output": {
                "location": "file2",
                "template": "file3"
            }
        }
        self.config.fix_all_path(sample, "/root/path")
        self.assertEqual("/root/path/directory", sample["input"]["directories"][0])
        self.assertEqual("/root/path/directory2/subdirectory", sample["input"]["directories"][1])
        self.assertEqual("/root/path/file", sample["input"]["files"][0])
        self.assertEqual("/root/path/directory/file", sample["input"]["files"][1])
        self.assertEqual("/root/path/file2", sample["output"]["location"])
        self.assertEqual("/root/path/file3", sample["output"]["template"])

    def test_fix_all_path__empty_datas(self):
        sample = {
            "input": {
                "directories": None,
                "files": None
            },
            "output": {
                "location": "file2",
                "template": "file3"
            }
        }
        self.config.fix_all_path(sample, "/root/path")
        self.assertEqual(None, sample["input"]["directories"])
        self.assertEqual(None, sample["input"]["files"])

    def test_fix_all_path__empty_output(self):
        sample = {
            "input": {
                "directories": None,
                "files": None
            },
            "output": {
                "location": "stdout",
                "template": "default"
            }
        }
        self.config.fix_all_path(sample, "/root/path")
        self.assertEqual("stdout", sample["output"]["location"])
        self.assertEqual("default", sample["output"]["template"])

    def test_fix_path__None(self):
        self.assertEqual(None, self.config.fix_path(None, "root"))

    def test_fix_path__file_missing(self):
        self.assertEqual("/root/sub/path/file", self.config.fix_path("path/file", "/root/sub"))

    def test_fix_path__file_exists(self):
        self.assertEqual(__file__, self.config.fix_path(__file__, "root"))
