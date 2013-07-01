from copy import deepcopy

from apidoc.service.validator import Validator
from apidoc.service.parser import Parser
from apidoc.service.merger import Merger
from apidoc.service.extender import Extender

from apidoc.factory.source.root import Root as RootFactory
from apidoc.factory.source.rootDto import RootDto as RootDtoFactory

from apidoc.object.source_raw import ObjectObject, Category

from apidoc.lib.util.decorator import add_property


@add_property("validator", Validator)
@add_property("parser", Parser)
@add_property("merger", Merger)
@add_property("extender", Extender)
@add_property("root_source_factory", RootFactory)
@add_property("root_dto_factory", RootDtoFactory)
class Source():

    """Create source object
    """

    extender_paths = (
        "categories/?",
        "versions/?",
        "versions/?/methods/?",
        "versions/?/types/?",
        "versions/?/references/?",
    )

    def create_from_config(self, config):
        """ Create a well populated Root object
        """

        raw_sources = self.get_sources_from_config(config)
        sources = self.format_sources_from_config(raw_sources, config)

        if config["input"]["validate"]:
            self.validator.validate_sources(sources)

        root = self.root_source_factory.create_from_dictionary(sources)
        self.replace_references(root)

        self.add_missing_categories(root)

        self.hide_filtered_elements(root, config["filter"])
        self.remove_hidden_elements(root)
        self.remove_unused_types(root)

        self.replace_types(root)

        return self.root_dto_factory.create_from_root(root)

    def format_sources_from_config(self, raw_sources, config):
        """ Create a well populated Root object
        """

        merged_source = self.merger.merge_sources(raw_sources)
        merged_source = self.inject_arguments_in_sources(merged_source, config["input"]["arguments"])

        return self.extender.extends(merged_source, paths=self.extender_paths)

    def get_sources_from_config(self, config):
        """Load a set of source's file defined in the config
        """
        sources = []
        if (config["input"]["directories"] is not None):
            for directory in config["input"]["directories"]:
                sources.extend(self.parser.load_all_from_directory(directory))
        if (config["input"]["files"] is not None):
            for file in config["input"]["files"]:
                sources.append(self.parser.load_from_file(file))
        return sources

    def inject_arguments_in_sources(self, sources, arguments):
        """ replace arguments in sources
        """
        if arguments is not None:
            for (argument, value) in arguments.items():
                sources = self.replace_argument(sources, argument, value)

        return sources

    def replace_argument(self, element, argument, value):
        """Replace sources arguments by value injected in config
        """
        if isinstance(element, list):
            return [self.replace_argument(x, argument, value) for x in element]
        elif isinstance(element, dict):
            return dict((x, self.replace_argument(y, argument, value)) for (x, y) in element.items())
        elif isinstance(element, str):
            return element.replace("${%s}" % argument, value)
        else:
            return element

    def hide_filtered_elements(self, root, config_filter):
        """Remove filter defined in config
        """
        if (config_filter["versions"]["includes"] is not None):
            for version in (version for version in root.versions.values() if version.name not in config_filter["versions"]["includes"]):
                version.display = False
        if (config_filter["versions"]["excludes"] is not None):
            for version in (version for version in root.versions.values() if version.name in config_filter["versions"]["excludes"]):
                version.display = False
        if (config_filter["categories"]["includes"] is not None):
            for category in (category for category in root.categories.values() if category.name not in config_filter["categories"]["includes"]):
                category.display = False
        if (config_filter["categories"]["excludes"] is not None):
            for category in (category for category in root.categories.values() if category.name in config_filter["categories"]["excludes"]):
                category.display = False

    def remove_unused_types(self, root):
        used_types = self.get_used_types(root)
        for version in root.versions.values():
            version.types = dict((type_name, type_value) for type_name, type_value in version.types.items() if type_name in used_types)

    def remove_hidden_elements(self, root):
        """Remove elements marked a not to display
        """
        root.versions = dict((x, y) for x, y in root.versions.items() if y.display)
        hidden_categories = [category.name for category in root.categories.values() if not category.display]
        for version in root.versions.values():
            version.methods = dict((x, y) for x, y in version.methods.items() if y.display and y.category not in hidden_categories)

    def add_missing_categories(self, root):
        """Remove elements marked a not to display
        """

        categories = [method.category for version in root.versions.values() for method in version.methods.values() if method.category not in root.categories.keys()] + \
            [type.category for version in root.versions.values() for type in version.types.values() if type.category not in root.categories.keys()]

        for category_name in categories:
            root.categories[category_name] = Category(category_name)

    def replace_references(self, root):
        """Remove elements marked a not to display
        """

        for version in root.versions.values():
            for method in version.methods.values():
                method.request_body = self.replace_references_in_object(method.request_body, version.references)
                method.response_body = self.replace_references_in_object(method.response_body, version.references)
            for type in version.types.values():
                type.item = self.replace_references_in_object(type.item, version.references)

    def replace_types(self, root):
        """Remove elements marked a not to display
        """

        for version in root.versions.values():
            for method in version.methods.values():
                method.request_body = self.replace_types_in_object(method.request_body, version.types)
                method.response_body = self.replace_types_in_object(method.response_body, version.types)
                for parameter in method.request_parameters.values():
                    self.replace_types_in_parameter(parameter, version.types)
                for parameter in method.request_headers.values():
                    self.replace_types_in_parameter(parameter, version.types)
            for type in version.types.values():
                type.item = self.replace_types_in_object(type.item, version.types)

    def replace_references_in_object(self, object, references):
        """Remove elements marked a not to display
        """

        if object is None:
            return object

        if object.type is ObjectObject.Types.reference:
            object = self.get_reference(object, references)
            self.replace_references_in_object(object, references)
        elif object.type is ObjectObject.Types.array:
            object.items = self.replace_references_in_object(object.items, references)
        elif object.type is ObjectObject.Types.dynamic:
            object.items = self.replace_references_in_object(object.items, references)
        elif object.type is ObjectObject.Types.object:
            for (property_name, property_value) in object.properties.items():
                object.properties[property_name] = self.replace_references_in_object(property_value, references)

        return object

    def replace_types_in_object(self, object, types):
        """Remove elements marked a not to display
        """

        if object is None:
            return object

        if object.type is ObjectObject.Types.type:
            if not object.type_name in types.keys():
                raise ValueError("Type \"%s\" unknow" % object.type_name)
            object.type_object = types[object.type_name]
        elif object.type is ObjectObject.Types.array:
            object.items = self.replace_types_in_object(object.items, types)
        elif object.type is ObjectObject.Types.dynamic:
            object.items = self.replace_types_in_object(object.items, types)
        elif object.type is ObjectObject.Types.object:
            for (property_name, property_value) in object.properties.items():
                object.properties[property_name] = self.replace_types_in_object(property_value, types)

        return object

    def replace_types_in_parameter(self, parameter, types):
        if parameter.type not in ObjectObject.Types:
            parameter.type_object = types[parameter.type]

        return parameter

    def get_used_types(self, root):
        types = []
        for version in root.versions.values():
            for method in version.methods.values():
                types += self.get_used_types_in_object(method.request_body)
                types += self.get_used_types_in_object(method.response_body)
                types += [parameter.type for parameter in method.request_parameters.values() if parameter.type not in ObjectObject.Types]
                types += [parameter.type for parameter in method.request_headers.values() if parameter.type not in ObjectObject.Types]
        return list({}.fromkeys(types).keys())

    def get_used_types_in_object(self, object):
        """Remove elements marked a not to display
        """
        types = []

        if object is None:
            return types

        if object.type is ObjectObject.Types.type:
            types += [object.type_name]
        elif object.type is ObjectObject.Types.array:
            types += self.get_used_types_in_object(object.items)
        elif object.type is ObjectObject.Types.dynamic:
            types += self.get_used_types_in_object(object.items)
        elif object.type is ObjectObject.Types.object:
            for property in object.properties.values():
                types += self.get_used_types_in_object(property)

        return types

    def get_reference(self, object, references):
        reference = deepcopy(references[object.reference_name])

        reference.name = object.name
        reference.optional = object.optional
        if object.description is not None:
            reference.description = object.description

        if reference.type is ObjectObject.Types.reference:
            return self.get_reference(reference, references)

        return reference
