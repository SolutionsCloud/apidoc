import sys
import argparse

from apidoc.factory.config import Config as ConfigFactory
from apidoc.service.config import Config as ConfigService
from apidoc.object.config import Config as ConfigObject


class Base():

    """Base command-line interface for ApiDoc
    """

    def __init__(self):
        """Initialyze the command
        """
        self.parser = argparse.ArgumentParser(description=self.__doc__)
        self.parser.add_argument(
            "-c", "--config", type=str, metavar="CONFIG",
            help="configuration file"
        )
        self.parser.add_argument(
            "-d", "--directories", nargs='+', type=str, metavar="DIRECTORY",
            help="directories containing documentation\'s source files"
        )
        self.parser.add_argument(
            "-f", "--files", nargs='+', type=str, metavar="FILE",
            help="documentation\'s source file"
        )
        self.parser.add_argument(
            "-o", "--output", type=str, metavar="FILE",
            help="rendered output file"
        )
        self.parser.add_argument(
            "-v", "--version", action='version', version='%(prog)s 1.0'
        )

    def get_config(self):
        """return command's configuration from call's arguments
        """
        options = self.parser.parse_args()

        if options.config is None and options.directories is None and options.files is None:
            self.parser.print_help()
            sys.exit(2)

        if options.config is not None:
            configFactory = ConfigFactory()
            config = configFactory.load_from_file(options.config)
        else:
            config = ConfigObject()

        if options.directories is not None:
            config["input"]["directories"] = [str(x) for x in options.directories]

        if options.files is not None:
            config["input"]["files"] = [str(x) for x in options.files]

        if options.output is not None:
            config["output"]["location"] = options.output

        configService = ConfigService()
        configService.validate(config)
        return config

    def main(self):
        """Run the command
        """
        raise NotImplementedError()
