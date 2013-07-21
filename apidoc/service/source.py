import logging
import re

from apidoc.object.source_dto import Root


class Source():

    """Provide tool to managed sources
    """

    def validate(self, sources):
        """Validate the format of sources
        """
        if not isinstance(sources, Root):
            raise Exception("Source object expected")

        parameters = self.get_uri_with_missing_parameters(sources)
        for parameter in parameters:
            logging.getLogger().warn('Missing parameter "%s" in uri of method "%s" in versions "%s"' % (parameter["name"], parameter["method"], parameter["version"]))

    def get_uri_with_missing_parameters(self, sources):
        parameters = []
        parameter_re = re.compile('\{([^}]+)\}')

        for method in [method for category in sources.method_categories for method in category.methods]:
            for uri_version in method.full_uri:
                for version in uri_version.versions:
                    method_parameters = [method_parameters_version.value.name for method_parameters_version in method.request_parameters if version in method_parameters_version.versions]
                    for missing_parameter in set(parameter_re.findall(uri_version.value)).difference(method_parameters):
                        parameters.append({"uri": uri_version.value, "name": missing_parameter, "method": method.name, "version": version})
                        #print(uri_parameter)

        return parameters
