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
        schema_file = os.path.join("apidoc", "datas", "schemas", "sources.yml")
        schema = self.parser.load_from_file(schema_file)

        from jsonschema import validate
        validate(sources, schema)

        #validator = Draft4Validator(schema)
        #errors = validator.iter_errors(sources)
        #for error in errors:
        #    logging.getLogger().warn("%s: %s" % ("/".join(list(error.path)), error.context[0] if error.context else error.message))
