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

        if not config["output"]["componants"] in ("local", "remote", "embedded"):
            raise ValueError("Unknown componant \"%s\"." % config["componants"])

        if config["input"]["directories"] is not None:
            unknown_directories = [x for x in config["input"]["directories"] if not os.path.isdir(x)]
            if len(unknown_directories) > 0:
                raise Exception(
                    "Director%s \"%s\" does not exists"
                    % ("ies" if len(unknown_directories) > 1 else "y", ("\" and \"").join(unknown_directories))
                )

            config["input"]["directories"] = [os.path.realpath(x) for x in config["input"]["directories"]]

        if config["input"]["files"] is not None:
            unknown_files = [x for x in config["input"]["files"] if not os.path.isfile(x)]
            if len(unknown_files) > 0:
                raise Exception(
                    "File%s \"%s\" does not exists"
                    % ("s" if len(unknown_files) > 1 else "", ("\" and \"").join(unknown_files))
                )

        if config["input"]["arguments"] is not None:
            if not isinstance(config["input"]["arguments"], dict):
                raise Exception(
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
