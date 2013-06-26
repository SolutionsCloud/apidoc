import unittest
import logging

from mock import patch

from apidoc.service.validator import Validator


class TestValidator(unittest.TestCase):

    def setUp(self):
        self.validator = Validator()

    @patch.object(logging.RootLogger, "warn")
    def test_load_from_source___log_errors(self, mock_logger):
        with patch("logging.getLogger", return_value=mock_logger):
            self.validator.validate_sources({"foo": "bar"})
            mock_logger.assert_called_once()
