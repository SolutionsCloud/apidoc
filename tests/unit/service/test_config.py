import os
import unittest

from apidoc.service.config import Config as ConfigService
from apidoc.object.config import Config


class TestConfig(unittest.TestCase):

    def setUp(self):
        self.config = ConfigService()

    def test_validate__nothing(self):
        with self.assertRaises(Exception):
            self.config.validate("foo")

    def test_validate__wrong_componant(self):
        config = Config()
        config["output"]["componants"] = "bla"
        with self.assertRaises(ValueError):
            self.config.validate(config)

    def test_validate__wrong_layout(self):
        config = Config()
        config["output"]["layout"] = "bla"
        with self.assertRaises(ValueError):
            self.config.validate(config)

    def test_validate__wrong_directories(self):
        config = Config()
        config["input"]["directories"] = ["bla"]
        with self.assertRaises(ValueError):
            self.config.validate(config)

    def test_validate__wrong_file(self):
        config = Config()
        config["input"]["files"] = ["bla"]
        with self.assertRaises(ValueError):
            self.config.validate(config)

    def test_validate__wrong_arguments(self):
        config = Config()
        config["input"]["arguments"] = ["bla"]
        with self.assertRaises(ValueError):
            self.config.validate(config)

    def test_validate(self):
        config = Config()
        config["output"]["componants"] = "local"
        config["output"]["layout"] = "default"
        config["input"]["directories"] = [os.path.dirname(__file__)]
        config["input"]["files"] = [__file__]
        config["input"]["arguments"] = {"foo": "bar"}

        self.config.validate(config)

    def test_validate__empty(self):
        self.config.validate(Config())

    def test_get_template_from_config__default(self):
        config = Config()
        config["output"]["template"] = "default"
        response = self.config.get_template_from_config(config)

        self.assertIsNotNone(response)

    def test_get_template_from_config__file(self):
        config = Config()
        config["output"]["template"] = __file__
        response = self.config.get_template_from_config(config)

        self.assertIsNotNone(response)
