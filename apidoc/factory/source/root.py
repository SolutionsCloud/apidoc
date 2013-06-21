from apidoc.object.source_raw import Root as ObjectRoot

from apidoc.factory.source.configuration import Configuration as ConfigurationFactory
from apidoc.factory.source.category import Category as CategoryFactory
from apidoc.factory.source.version import Version as VersionFactory

from apidoc.lib.util.decorator import add_property


@add_property("configuration_factory", ConfigurationFactory)
@add_property("category_factory", CategoryFactory)
@add_property("version_factory", VersionFactory)
class Root():
    """ Root Factory
    """

    def create_from_dictionary(self, datas):
        """Return a populated Object Root from dictionnary datas
        """
        root = ObjectRoot()

        if "configuration" in datas and datas["configuration"] is not None:
            root.configuration = self.configuration_factory.create_from_dictionary(datas["configuration"])

        if "categories" in datas and datas["categories"] is not None:
            root.categories = self.category_factory.create_dictionary_of_element_from_dictionary("categories", datas)

        root.versions = self.version_factory.create_dictionary_of_element_from_dictionary("versions", datas)

        for version in root.versions.values():
            version.full_uri = "%s%s" % (root.configuration.uri or "", version.uri or "")
            for method in version.methods.values():
                method.absolute_uri = "%s%s" % (version.uri or "", method.uri or "")
                method.full_uri = "%s%s" % (version.full_uri or "", method.uri or "")

        return root
