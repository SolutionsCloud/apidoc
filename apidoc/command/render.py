#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from apidoc.command.base import Base
from apidoc.factory.source import Source as SourceFactory
from apidoc.factory.template import Template as TemplateFactory
from apidoc.service.source import Source as SourceService


class Render(Base):

    """Build documentation from sources files
    """

    def main(self):
        """Run the command
        """
        sourceService = SourceService()
        sourceFactory = SourceFactory()
        templateFactory = TemplateFactory()

        config = self.get_config()

        sources = sourceFactory.create_from_config(config)
        sourceService.validate(sources)

        template = templateFactory.create_from_config(config)
        template.render(sources, config)


def main():
    """Main function to run command
    """
    Render().main()

if __name__ == '__main__':
    main()
