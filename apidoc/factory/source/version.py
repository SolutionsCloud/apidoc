from apidoc.object.source_raw import Version as ObjectVersion

from apidoc.factory.source.element import Element as ElementFactory
from apidoc.factory.source.method import Method as MethodFactory
from apidoc.factory.source.type import Type as TypeFactory
from apidoc.factory.source.object import Object as ObjectFactory

from apidoc.lib.util.decorator import add_property


@add_property("method_factory", MethodFactory)
@add_property("type_factory", TypeFactory)
@add_property("reference_factory", ObjectFactory)
class Version(ElementFactory):
    """ Version Factory
    """

    def create_from_name_and_dictionary(self, name, datas):
        """Return a populated object Version from dictionary datas
        """
        version = ObjectVersion()
        self.set_common_datas(version, name, datas)

        if "uri" in datas:
            version.uri = str(datas["uri"])
        if "major" in datas:
            version.major = int(datas["major"])
        if "minor" in datas:
            version.minor = int(datas["minor"])
        if "status" in datas:
            version.status = self.get_enum("status", ObjectVersion.Status, datas)

        version.methods = self.method_factory.create_dictionary_of_element_from_dictionary("methods", datas)
        version.types = self.type_factory.create_dictionary_of_element_from_dictionary("types", datas)
        version.references = self.reference_factory.create_dictionary_of_element_from_dictionary("references", datas)

        return version
