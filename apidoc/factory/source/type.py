from apidoc.object.source_raw import Type as ObjectType

from apidoc.factory.source.element import Element as ElementFactory
from apidoc.factory.source.object import Object as ObjectFactory

from apidoc.lib.util.decorator import add_property


@add_property("object_factory", ObjectFactory)
class Type(ElementFactory):
    """ Type Factory
    """

    def create_from_name_and_dictionary(self, name, datas):
        """Return a populated object Type from dictionary datas
        """
        if not "item" in datas:
            raise ValueError("An item must be set in type \"%s\"." % name)

        type = ObjectType()
        self.set_common_datas(type, name, datas)

        type.item = self.object_factory.create_from_name_and_dictionary(type.name, datas["item"])

        if "category" in datas:
            type.category = str(datas["category"])
        else:
            type.category = None

        if "format" in datas and datas["format"] is not None:
            if "pretty" in datas["format"]:
                type.format.pretty = str(datas["format"]["pretty"])
            if "advanced" in datas["format"]:
                type.format.advanced = str(datas["format"]["advanced"])

        return type
