#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import traceback
import time

from datetime import datetime

from apidoc.lib.fswatcher.observer import Observer
from apidoc.lib.fswatcher.callbackHandler import CallbackHandler
from apidoc.command.base import Base
from apidoc.factory.source import Source as SourceFactory
from apidoc.factory.template import Template as TemplateFactory
from apidoc.service.source import Source as SourceService
from apidoc.service.config import Config as ConfigService


class Watch(Base):
    """Build documentation from sources each time a source or template files is modified
    """

    def main(self):
        """Run the command
        """
        configService = ConfigService()

        self.config = self.get_config()

        self.refresh_source(None)

        #todo replace print by logs
        print("%s - Start watching" % datetime.now().time().isoformat())

        observer = Observer()

        template_handler = CallbackHandler(self.refresh_template)
        source_handler = CallbackHandler(self.refresh_source)

        template_path = os.path.dirname(configService.get_template_from_config(self.config))
        observer.add_handler(template_path, template_handler)

        if (self.config["input"]["directories"] is not None):
            for directory in self.config["input"]["directories"]:
                observer.add_handler(directory, source_handler)

        if (self.config["input"]["files"] is not None):
            for file in self.config["input"]["files"]:
                observer.add_handler(file, source_handler)

        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

    def refresh_source(self, event):
        """Refresh sources then templates
        """
        now = datetime.now()
        print("%s - Sources changed..." % now.time().isoformat())

        sourceFactory = SourceFactory()
        sourceService = SourceService()
        templateFactory = TemplateFactory()

        try:
            self.sources = sourceFactory.load_from_config(self.config)
            sourceService.validate(self.sources)

            template = templateFactory.create_from_config(self.config)
            template.render(self.sources, self.config)
            print("rendered in %s." % (datetime.now() - now))
        except:
            print("Failed to render")
            print(traceback.format_exc())

    def refresh_template(self, event):
        """Refresh template's contents
        """
        now = datetime.now()
        print("%s - Template changed..." % now.time().isoformat())
        templateFactory = TemplateFactory()

        try:
            template = templateFactory.create_from_config(self.config)
            template.render(self.sources, self.config)
            print("rendered in %s." % (datetime.now() - now))
        except:
            print("Failed to render")
            print(traceback.format_exc())


if __name__ == '__main__':
    Watch().main()
