import collections

from apidoc.object.source_raw import Sampleable, Displayable

from apidoc.lib.util.cast import to_boolean


class Element():
    """ Populate Helper Factory
    """

    def set_common_datas(self, element, name, datas):
        """Populated common data for an element from dictionnary datas
        """
        element.name = str(name)
        if "description" in datas:
            element.description = str(datas["description"]).strip()

        if isinstance(element, Sampleable) and element.sample is None and "sample" in datas:
            element.sample = str(datas["sample"]).strip()

        if isinstance(element, Displayable):
            if "display" in datas:
                element.display = to_boolean(datas["display"])

            if "label" in datas:
                element.label = datas["label"]
            else:
                element.label = element.name

    def create_dictionary_of_element_from_dictionary(self, property_name, datas):
        """Populate a dictionary of elements
        """
        response = {}
        if property_name in datas and datas[property_name] is not None and isinstance(datas[property_name], collections.Iterable):
            for key, value in datas[property_name].items():
                response[key] = self.create_from_name_and_dictionary(key, value)

        return response

    def create_list_of_element_from_dictionary(self, property_name, datas):
        """Populate a list of elements
        """
        response = []
        if property_name in datas and datas[property_name] is not None and isinstance(datas[property_name], list):
            for value in datas[property_name]:
                response.append(self.create_from_dictionary(value))

        return response

    def get_enum(self, property, enum, datas):
        """Factory enum type
        """
        str_property = str(datas[property]).lower()
        if not str_property in enum:
            raise ValueError("Unknow enum \"%s\" for \"%s\"." % (str_property, property))
        return enum(str_property)
