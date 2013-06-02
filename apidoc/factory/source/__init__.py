from apidoc.service.parser import Parser
from apidoc.service.merger import Merger
from apidoc.service.extender import Extender

from apidoc.factory.source.root import Root as RootFactory
from apidoc.factory.source.rootDto import RootDto as RootDtoFactory

from apidoc.lib.util.decorator import add_property


@add_property("parser", Parser)
@add_property("merger", Merger)
@add_property("extender", Extender)
@add_property("root_source_factory", RootFactory)
@add_property("root_dto_factory", RootDtoFactory)
class Source():

    """Create source objet
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

        root = self.root_source_factory.create_from_dictionary(sources)

        self.hide_filtered_elements(root, config["filter"])
        self.remove_hidden_elements(root)

        return self.root_dto_factory.create_from_root(root)

    def format_sources_from_config(self, raw_sources, config):
        """ Create a well populated Root object
        """

        merged_source = self.merger.merge_sources(raw_sources)
        self.inject_arguments_in_sources(merged_source, config["input"]["arguments"])
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

    def remove_hidden_elements(self, root):
        """Remove elements marked a not to display
        """
        root.versions = dict((x, y) for x, y in root.versions.items() if y.display)
        hidden_categories = [category.name for category in root.categories.values() if not category.display]
        for version in root.versions.values():
            version.methods = dict((x, y) for x, y in version.methods.items() if y.display and (y.category is None or y.category not in hidden_categories))
