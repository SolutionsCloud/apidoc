#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from apidoc.command.base import Base
from apidoc.factory.source import Source as SourceFactory
from apidoc.service.source import Source as SourceService
from apidoc.lib.util.serialize import json_repr


class Analyse(Base):

    """Analyse sources files for ApiDoc and print the formated result
    """

    def main(self):
        """Run the command
        """
        sourceService = SourceService()
        sourceFactory = SourceFactory()

        config = self.get_config()
        sources = sourceFactory.create_from_config(config)
        sourceService.validate(sources)

        print(json_repr(sources))


def main():
    """Main function to run command
    """
    Analyse().main()

if __name__ == '__main__':
    main()
