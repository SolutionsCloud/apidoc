from apidoc.object.source import MethodCategory, TypeCategory
from apidoc.object.source import MethodCrossVersion, TypeCrossVersion, ElementCrossVersion
from apidoc.service.parser import Parser
from apidoc.service.merger import Merger
from apidoc.service.extender import Extender

from apidoc.factory.source.root import Root as RootFactory

from apidoc.lib.util.decorator import add_property


@add_property("parser", Parser)
@add_property("merger", Merger)
@add_property("extender", Extender)
@add_property("root_factory", RootFactory)
class Source():

    """Create source objet
    """

    def create_from_config(self, config):
        """ Create a well populated Root object
        """
        raw_sources = self.get_sources_from_config(config)
        merged_source = self.merger.merge_sources(raw_sources)
        self.inject_arguments_in_sources_from_config(merged_source, config)
        extended_sources = self.extender.extends(merged_source, paths=self.get_extender_paths())

        root = self.root_factory.create_from_dictionary(extended_sources)

        self.apply_config_filter(root, config["filter"])
        self.remove_undisplayed(root)
        self.fix_versions(root)
        self.refactor_hierarchy(root)

        return root

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

    def inject_arguments_in_sources_from_config(self, sources, config):
        """ replace arguments in sources
        """
        if config["input"]["arguments"] is not None:
            for (argument, value) in config["input"]["arguments"].items():
                sources = self.replace_argument(sources, argument, value)

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

    def apply_config_filter(self, root, config_filter):
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

    def remove_undisplayed(self, root):
        """Remove elements marked a not to display
        """
        root.versions = dict((x, y) for x, y in root.versions.items() if y.display)
        displayed_categories = [category.name for category in root.categories.values() if category.display]
        for version in root.versions.values():
            version.methods = dict((x, y) for x, y in version.methods.items() if y.display and (y.category is None or y.category in displayed_categories))

    def fix_versions(self, root):
        """Set the version of elements
        """
        for (version_name, version) in root.versions.items():
            for (type_name, type) in version.types.items():
                type.version = version_name
            for (reference_name, reference) in version.references.items():
                reference.version = version_name
            for (method_name, method) in version.methods.items():
                method.version = version_name

    def refactor_hierarchy(self, root):
        """Modify elements structure (root/version/elements/) to (root/elementByVersion/element)
            Todo: This method is not solid
        """
        root.methods = {}
        root.method_categories = {}
        root.types = {}
        root.type_categories = {}
        root.references = {}
        for (version_name, version) in root.versions.items():
            for (reference_name, reference) in version.references.items():
                if reference_name not in root.references:
                    root.references[reference_name] = ElementCrossVersion(element=reference)
                root.references[reference_name].versions[version_name] = reference

            for (type_name, type) in version.types.items():
                if type.category not in root.type_categories:
                    root.type_categories[type.category] = TypeCategory(name=type.category)
                    if type.category in root.categories:
                        root.type_categories[type.category].order = root.categories[type.category].order
                        root.type_categories[type.category].description = root.categories[type.category].description

                if type_name not in root.type_categories[type.category].types:
                    root.type_categories[type.category].types[type_name] = TypeCrossVersion(element=type)
                root.type_categories[type.category].types[type_name].versions[version_name] = type

                if type.signature not in root.type_categories[type.category].types[type_name].signatures:
                    root.type_categories[type.category].types[type_name].signatures[type.signature] = type

                if type_name not in root.types:
                    root.types[type_name] = TypeCrossVersion(element=type)
                root.types[type_name].versions[version_name] = type

            for (method_name, method) in version.methods.items():
                if method.category not in root.method_categories:
                    root.method_categories[method.category] = MethodCategory(name=method.category)
                    if method.category in root.categories:
                        root.method_categories[method.category].order = root.categories[method.category].order
                        root.method_categories[method.category].description = root.categories[method.category].description

                if method_name not in root.method_categories[method.category].methods:
                    root.method_categories[method.category].methods[method_name] = MethodCrossVersion(element=method)
                root.method_categories[method.category].methods[method_name].versions[version_name] = method

                if method.signature not in root.method_categories[method.category].methods[method_name].signatures:
                    root.method_categories[method.category].methods[method_name].signatures[method.signature] = method

                if method_name not in root.methods:
                    root.methods[method_name] = MethodCrossVersion(element=method)
                root.methods[method_name].versions[version_name] = method

            del(version.methods)
            del(version.types)
            del(version.references)

    def get_extender_paths(self):
        """Retrieve extension lookup path
        """
        return (
            "categories/?",
            "versions/?",
            "versions/?/methods/?",
            "versions/?/types/?",
            "versions/?/references/?",
        )
