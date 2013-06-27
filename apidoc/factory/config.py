import os

from apidoc.object.config import Config as ConfigObject
from apidoc.service.parser import Parser
from apidoc.service.merger import Merger
from apidoc.service.validator import Validator

from apidoc.lib.util.decorator import add_property


@add_property("validator", Validator)
@add_property("parser", Parser)
@add_property("merger", Merger)
class Config():
    """Create config objects
    """

    def load_from_file(self, config_file):
        """Load a config object from a file
        """
        merger = self.merger
        parser = self.parser

        datas = parser.load_from_file(config_file)
        self.validator.validate_config(datas)

        if datas is None or datas == {}:
            config = ConfigObject()
        else:
            config = merger.merge_configs(ConfigObject(), [datas])

        self.fix_all_path(config, os.path.dirname(config_file))
        return config

    def fix_all_path(self, config, root_path):
        """Fix config's content's relative path by injecting config location
        """
        if config["input"]["directories"] is not None:
            config["input"]["directories"] = [
                self.fix_path(x, root_path) for x in config["input"]["directories"]
            ]
        if config["input"]["files"] is not None:
            config["input"]["files"] = [self.fix_path(x, root_path) for x in config["input"]["files"]]
        if not config["output"]["location"] in ("stdout"):
            config["output"]["location"] = self.fix_path(config["output"]["location"], root_path)
        if not config["output"]["template"] in ("default"):
            config["output"]["template"] = self.fix_path(config["output"]["template"], root_path)

    def fix_path(self, path, root_path):
        """Fix a relative path
        """
        if path is not None:
            if not os.path.exists(path):
                path = os.path.realpath(os.path.join(root_path, path))
        return path
