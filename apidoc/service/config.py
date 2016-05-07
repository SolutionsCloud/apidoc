import os
from apidoc.object.config import Config as ConfigObject


class Config():

    """Provide tool to managed config
    """

    def validate(self, config):
        """Validate that the source file is ok
        """
        if not isinstance(config, ConfigObject):
            raise Exception("Config object expected")

        if config["output"]["componants"] not in ("local", "remote", "embedded", "without"):
            raise ValueError("Unknown componant \"%s\"." % config["output"]["componants"])

        if config["output"]["layout"] not in ("default", "content-only"):
            raise ValueError("Unknown layout \"%s\"." % config["output"]["layout"])

        if config["input"]["locations"] is not None:
            unknown_locations = [x for x in config["input"]["locations"] if not os.path.exists(x)]
            if len(unknown_locations) > 0:
                raise ValueError(
                    "Location%s \"%s\" does not exists"
                    % ("s" if len(unknown_locations) > 1 else "", ("\" and \"").join(unknown_locations))
                )

            config["input"]["locations"] = [os.path.realpath(x) for x in config["input"]["locations"]]

        if config["input"]["arguments"] is not None:
            if not isinstance(config["input"]["arguments"], dict):
                raise ValueError(
                    "Sources arguments \"%s\" are not a dict" % config["input"]["arguments"]
                )

    def get_template_from_config(self, config):
        """Retrieve a template path from the config object
        """
        if config["output"]["template"] == "default":
            return os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                'template',
                'default.html'
            )
        else:
            return os.path.abspath(config["output"]["template"])
