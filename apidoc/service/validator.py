import os
import logging

from jsonschema import Draft4Validator

from apidoc.service.parser import Parser

from apidoc.lib.util.decorator import add_property


@add_property("parser", Parser)
class Validator():

    """Validate a source schema
    """
    def validate_sources(self, sources):
        schema_location = os.path.join(os.path.dirname(__file__), "..", "..", "apidoc", "datas", "schemas", "source.yml")
        self.validate_schema(schema_location, sources)

    """Validate a config schema
    """
    def validate_config(self, config):
        schema_location = os.path.join(os.path.dirname(__file__), "..", "..", "apidoc", "datas", "schemas", "config.yml")
        self.validate_schema(schema_location, config)

    """Validate a schema
    """
    def validate_schema(self, schema_location, input):
        schema = self.parser.load_from_file(schema_location)

        validator = Draft4Validator(schema)
        errors = validator.iter_errors(input)
        for error in errors:
            logging.getLogger().warn("%s: %s" % ("/".join([str(x) for x in error.path]), error.context[0] if error.context else error.message))
