from apidoc.object.source_raw import EnumTypeValue as ObjecEnumValue

from apidoc.factory.source.element import Element as ElementFactory


class EnumValue(ElementFactory):
    """ EnumValue Factory
    """

    def create_from_name_and_dictionary(self, name, datas):
        """Return a populated object EnumValue from dictionary datas
        """
        enum_value = ObjecEnumValue()
        self.set_common_datas(enum_value, name, datas)

        return enum_value
