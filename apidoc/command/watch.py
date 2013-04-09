#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import traceback

import time
import threading

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

        event_handler = EventHandler(runner)

        observer = Observer(event_handler)

        template_path = os.path.dirname(configService.get_template_from_config(config))
        observer.watch(template_path)
        event_handler.types[template_path] = "template"

        if (config["input"]["directories"] is not None):
            for directory in config["input"]["directories"]:
                observer.watch(directory)
                event_handler.types[directory] = "source"

        if (config["input"]["files"] is not None):
            for file in config["input"]["files"]:
                observer.watch(file)
                event_handler.types[file] = "source"

        observer.loop()


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


class EventHandler():
    """Handle FileSystem modifications to refresh documentation
    """
    def __init__(self, runner):
        self.runner = runner
        self.types = {}

    def on_change(self, path):
        """Default handler
        """
        now = datetime.now()
        print("%s - Content changed..." % now.time().isoformat())
        try:
            if path in self.types:
                if self.types[path] == "source":
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


class Observer(threading.Thread):
    """Observe change in file FileSystem
    """
    def __init__(self, handler):
        """Class instantiation
        """
        super().__init__()
        self.paths = {}
        self.handler = handler
        self.terminated = False

    def watch(self, path):
        """Add a path in watch queue
        """
        self.paths[path] = self.path_sign(path)

    def path_sign(self, path):
        """generate a unique signature for file contained in path
        """
        if not os.path.exists(path):
            return None
        if os.path.isdir(path):
            merge = {}
            for root, dirs, files in os.walk(path):
                for name in files:
                    full_name = os.path.join(root, name)
                    merge[full_name] = os.stat(full_name)
            return merge
        else:
            return os.stat(path)

    def loop(self):
        """Run loop in a new thread
        """
        self.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
        self.join()

    def run(self):
        """Main loop of observer's thread. looks for changes in one of paths and call on_change of EventHandler
        """
        while not self.terminated:
            for (path, current_sign) in self.paths.items():
                new_sign = self.path_sign(path)
                if new_sign != current_sign:
                    self.paths[path] = new_sign
                    self.handler.on_change(path)
            time.sleep(0.2)

    def stop(self):
        """Stop thread loop
        """
        self.terminated = True


if __name__ == '__main__':
    Watch().main()
