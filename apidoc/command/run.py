#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import time
import logging
import logging.config
import argparse

from datetime import datetime

from apidoc import __version__

from apidoc.lib.fswatcher.observer import Observer
from apidoc.lib.fswatcher.callbackHandler import CallbackHandler
from apidoc.lib.util.serialize import json_repr

from apidoc.factory.config import Config as ConfigFactory
from apidoc.factory.source import Source as SourceFactory
from apidoc.factory.template import Template as TemplateFactory

from apidoc.object.config import Config as ConfigObject

from apidoc.service.source import Source as SourceService
from apidoc.service.config import Config as ConfigService
from apidoc.service.parser import Parser as FileParser


class ApiDoc():

    """Base command-line interface for ApiDoc
    """
    dry_run = False
    watch = False
    traceback = False
    config = None

    def __init__(self):
        """Initialyze the command
        """
        self.parser = argparse.ArgumentParser(description=self.__doc__)
        self.parser.add_argument(
            "-c", "--config", type=str, metavar="CONFIG",
            help="configuration file"
        )
        self.parser.add_argument(
            "-i", "--input", nargs='+', type=str, metavar="DIRECTORY OR FILE",
            help="directories and/or files containing documentation\'s source files"
        )
        self.parser.add_argument(
            "-o", "--output", type=str, metavar="FILE",
            help="rendered output file"
        )
        self.parser.add_argument(
            "-v", "--version", action='version', version='%(prog)s ' + __version__
        )
        self.parser.add_argument(
            "-n", "--no-validate", action='store_const', const=True,
            help="disable validation"
        )
        self.parser.add_argument(
            "-a", "--arguments", nargs='+', type=str, metavar="ARGUMENT",
            help="documentation\'s arguments arg1=value1 arg2=value2"
        )
        self.parser.add_argument(
            "-y", "--dry-run", action='store_const', const=True,
            help="analyse config's and source's files without building the documentation"
        )
        self.parser.add_argument(
            "-w", "--watch", action='store_const', const=True,
            help="re-render the documentation each time a source's file or a template's file changes"
        )
        self.parser.add_argument(
            "-q", "--quiet", action='store_const', const=True,
            help="does not display logging information below warning level"
        )
        self.parser.add_argument(
            "-qq", "--silence", action='store_const', const=True,
            help="does not display any logging information"
        )
        self.parser.add_argument(
            "-t", "--traceback", action='store_const', const=True,
            help="display traceback when an exception raised"
        )

        self.logger = logging.getLogger()

    def _init_config(self):
        """return command's configuration from call's arguments
        """
        options = self.parser.parse_args()
        if options.config is None and options.input is None:
            self.parser.print_help()
            sys.exit(2)

        if options.config is not None:
            configFactory = ConfigFactory()
            config = configFactory.load_from_file(options.config)
        else:
            config = ConfigObject()

        if options.input is not None:
            config["input"]["locations"] = [str(x) for x in options.input]
        if options.arguments is not None:
            config["input"]["arguments"] = dict((x.partition("=")[0], x.partition("=")[2]) for x in options.arguments)

        if options.output is not None:
            config["output"]["location"] = options.output

        if options.no_validate is not None:
            config["input"]["validate"] = not options.no_validate

        if options.dry_run is not None:
            self.dry_run = options.dry_run
        if options.watch is not None:
            self.watch = options.watch
        if options.traceback is not None:
            self.traceback = options.traceback

        if options.quiet is not None:
            self.logger.setLevel(logging.WARNING)
        if options.silence is not None:
            logging.disable(logging.CRITICAL)

        configService = ConfigService()
        configService.validate(config)
        self.config = config

    """Build documentation from sources each time a source or template files is modified
    """

    def main(self):
        """Run the command
        """
        self._init_config()

        if self.dry_run:
            return self.run_dry_run()
        elif self.watch:
            return self.run_watch()
        else:
            return self.run_render()

    def _get_sources(self):
        now = datetime.now()

        try:
            sourceService = SourceService()
            sourceFactory = SourceFactory()

            sources = sourceFactory.create_from_config(self.config)
            sourceService.validate(sources)

            self.logger.debug("Parse sources in %s." % (datetime.now() - now))
        except:
            if self.traceback:
                self.logger.exception("Failed to parse sources")
            else:
                self.logger.error("Failed to parse sources")
            raise

        return sources

    def _render_template(self, sources):
        now = datetime.now()

        try:
            templateFactory = TemplateFactory()

            template = templateFactory.create_from_config(self.config)
            template.render(sources, self.config)

            self.logger.debug("Render template in %s." % (datetime.now() - now))
        except:
            if self.traceback:
                self.logger.exception("Failed to render template")
            else:
                self.logger.error("Failed to render template")
            raise

    def run_dry_run(self):
        try:
            sources = self._get_sources()
        except:
            pass

        print(json_repr(sources))

    def run_render(self):
        try:
            sources = self._get_sources()
            self._render_template(sources)
        except:
            pass

    def run_watch(self):
        configService = ConfigService()

        self.logger.info("Start watching")
        self._watch_refresh_source(None)

        observer = Observer()

        template_handler = CallbackHandler(self._watch_refresh_template)
        source_handler = CallbackHandler(self._watch_refresh_source)

        template_path = os.path.dirname(configService.get_template_from_config(self.config))
        observer.add_handler(template_path, template_handler)

        if (self.config["input"]["locations"] is not None):
            for location in self.config["input"]["locations"]:
                observer.add_handler(location, source_handler)

        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

    def _watch_refresh_source(self, event):
        """Refresh sources then templates
        """
        self.logger.info("Sources changed...")

        try:
            self.sources = self._get_sources()
            self._render_template(self.sources)
        except:
            pass

    def _watch_refresh_template(self, event):
        """Refresh template's contents
        """
        self.logger.info("Template changed...")

        try:
            self._render_template(self.sources)
        except:
            pass


def main():
    """Main function to run command
    """
    configParser = FileParser()
    logging.config.dictConfig(
        configParser.load_from_file(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'settings', 'logging.yml'))
    )
    ApiDoc().main()

if __name__ == '__main__':
    main()
