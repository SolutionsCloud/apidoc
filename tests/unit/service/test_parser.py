import unittest

from mock import patch, call

from apidoc.service.parser import Parser
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


class TestParser(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()

    def test_load_from_file(self):
        with self.assertRaises(ValueError):
            self.parser.load_from_file("file_name", "abc")

        with self.assertRaises(ValueError):
            self.parser.load_from_file("file_name.abc")

        with patch("builtins.open", return_value="file_content") as mock_open:
            with patch("yaml.load", return_value="content_formated") as mock_yaml:
                self.assertEqual("content_formated", self.parser.load_from_file("file_name.yml"))

                mock_open.assert_called_once_with("file_name.yml")
                mock_yaml.assert_called_once_with("file_content", Loader=Loader)

        with patch("builtins.open", return_value="file_content") as mock_open:
            with patch("yaml.load", return_value="content_formated") as mock_yaml:
                self.assertEqual("content_formated", self.parser.load_from_file("file_name.yaml"))

                mock_open.assert_called_once_with("file_name.yaml")
                mock_yaml.assert_called_once_with("file_content", Loader=Loader)

        with patch("builtins.open", return_value="file_content") as mock_open:
            with patch("json.load", return_value="content_formated") as mock_json:
                self.assertEqual("content_formated", self.parser.load_from_file("file_name.json"))

                mock_open.assert_called_once_with("file_name.json")
                mock_json.assert_called_once_with("file_content")

        with patch("builtins.open", return_value="file_content") as mock_open:
            with patch("json.load", return_value="content_formated") as mock_json:
                self.assertEqual("content_formated", self.parser.load_from_file("file_name.yaml", "json"))

                mock_open.assert_called_once_with("file_name.yaml")
                mock_json.assert_called_once_with("file_content")

    @patch("os.walk", return_value=[('root', [], ['file1', 'file2']), ('root2', [], ['file3'])])
    @patch.object(Parser, "load_from_file", side_effect=[{"key": "first"}, {"second": "value"}, {"3": "third"}])
    def test_load_all_from_directory(self, mock_parser, mock_walk):
        response = self.parser.load_all_from_directory("directory")

        mock_walk.assert_called_once_with("directory")
        mock_parser.assert_has_calls([call('root/file1'), call('root/file2'), call('root2/file3')])
        self.assertEqual([{"key": "first"}, {"second": "value"}, {"3": "third"}], response)
