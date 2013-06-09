from apidoc.object.source_raw import Type as ObjectType
from apidoc.object.source_raw import EnumType as ObjectEnumType

from apidoc.factory.source.element import Element as ElementFactory
from apidoc.factory.source.enumValue import EnumValue as EnumValueFactory

from apidoc.lib.util.decorator import add_property


@add_property("enum_value_factory", EnumValueFactory)
class Type(ElementFactory):
    """ Type Factory
    """

    def create_from_name_and_dictionary(self, name, datas):
        """Return a populated object Type from dictionary datas
        """
        if "primary" in datas:
            primary = self.get_enum("primary", ObjectType.Primaries, datas)
        else:
            raise ValueError("A type\'s primary must be set in type \"%s\"." % name)

        if primary is ObjectType.Primaries.enum:
            type = ObjectEnumType()
        else:
            type = ObjectType()

        type.primary = primary
        self.set_common_datas(type, name, datas)

        if "category" in datas:
            type.category = str(datas["category"])
        else:
            type.category = None

        if "format" in datas and datas["format"] is not None:
            if "sample" in datas["format"]:
                type.format.sample = str(datas["format"]["sample"])
            if "pretty" in datas["format"]:
                type.format.pretty = str(datas["format"]["pretty"])
            if "advanced" in datas["format"]:
                type.format.advanced = str(datas["format"]["advanced"])

        if isinstance(type, ObjectEnumType):
            type.values = self.enum_value_factory.create_dictionary_of_element_from_dictionary("values", datas)

        return type
