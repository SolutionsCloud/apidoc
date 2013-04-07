#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import traceback
import pyinotify

from datetime import datetime

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

        config = self.get_config()

        runner = Runner(config)
        runner.refresh_sources()
        runner.refresh_template()

        #todo replace print by logs
        print("%s - Start watching" % datetime.now().time().isoformat())
        changeHandler = ChangeHandler(runner)

        wm = pyinotify.WatchManager()
        notifier = pyinotify.Notifier(wm, changeHandler)
        mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MODIFY
        template_path = os.path.dirname(configService.get_template_from_config(config))
        wm.add_watch(template_path, mask, rec=True)

        changeHandler.types[template_path] = "template"
        if (config["input"]["directories"] is not None):
            for directory in config["input"]["directories"]:
                wm.add_watch(directory, mask, rec=True)
                changeHandler.types[directory] = "source"
        if (config["input"]["files"] is not None):
            for file in config["input"]["files"]:
                wm.add_watch(file, mask)
                changeHandler.types[file] = "source"

        notifier.loop()


class Runner():
    """Object in charge of documentation rendering
    """

    def __init__(self, config):
        """Class instantiation
        """
        self.config = config

    def refresh_sources(self):
        """Refresh source contents
        """
        sourceFactory = SourceFactory()
        sourceService = SourceService()

        sources = sourceFactory.load_from_config(self.config)
        sourceService.validate(sources)
        self.sources = sources

    def refresh_template(self):
        """Refresh template's contents
        """
        templateFactory = TemplateFactory()

        template = templateFactory.create_from_config(self.config)
        template.render(self.sources, self.config)


class ChangeHandler(pyinotify.ProcessEvent):
    """Handle FileSystem modifications to refresh documentation
    """

    def __init__(self, runner):
        """Class instantiation
        """
        self.runner = runner
        self.types = {}

    def process_default(self, event):
        """Default handler
        """
        if event.dir:
            return
        if event.name[0:1] == ".":
            return

        now = datetime.now()
        print("%s - Content changed..." % now.time().isoformat())
        try:
            if event.path in self.types:
                if self.types[event.path] == "source":
                    self.runner.refresh_sources()
                    self.runner.refresh_template()
                else:
                    self.runner.refresh_template()
            else:
                self.runner.refresh_sources()
                self.runner.refresh_template()
            print("rendered in %s." % (datetime.now() - now))
        except:
            print("Failed to render")
            print(traceback.format_exc())


if __name__ == '__main__':
    Watch().main()
