import logging

from functools import total_ordering
from apidoc.lib.util.enum import Enum
from apidoc.object.source_raw import Object


class RootDto():

    """Root object of sources elements for templates
    """

    _instance = None

    @classmethod
    def instance(cls):
        """Retrieve the unique instance of the element
        """
        if RootDto._instance is None:
            RootDto._instance = RootDto()
        return RootDto._instance

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.configuration = None
        self.versions = []
        self.method_categories = []
        self.type_categories = []

    def get_used_type_categories(self):
        """return list of used type_categories
        """
        for category in [x for x in self.type_categories.values() if len(x.get_used_types()) == 0]:
            logging.getLogger().warn("Unused type category %s" % category.name)
        return [x for x in self.type_categories.values() if len(x.get_used_types()) > 0]

    def get_used_types(self):
        """return list of types used in a method
        """
        types = []
        for category in self.method_categories.values():
            for method_versioned in category.methods.values():
                for method in method_versioned.signatures.values():
                    types += method.get_used_types()
        return list({}.fromkeys(types).keys())


class ElementDto():

    """Element
    """

    def __init__(self, element):
        """Class instantiation
        """
        self.name = element.name
        self.description = element.description


class ElementVersionedDto():

    """Element
    """

    def __init__(self, element):
        """Class instantiation
        """
        self.name = element.name
        self.description = []


@total_ordering
class Comparable():

    """Element who can be sorted
    """

    def get_comparable_values(self):
        """Return a tupple of values representing the unicity of the object
        """
        return ()

    def get_comparable_values_for_equality(self):
        """Return a tupple of values representing the unicity of the object
        """
        return self.get_comparable_values()

    def get_comparable_values_for_ordering(self):
        """Return a tupple of values representing the unicity of the object
        """
        return self.get_comparable_values()

    def __lt__(self, other):
        """Return true if self is lower than other
        """
        return self.get_comparable_values_for_ordering() < other.get_comparable_values_for_ordering()

    def __eq__(self, other):
        """Return true if self is equals to other
        """
        return type(self) is type(other) and self.get_comparable_values_for_equality() == other.get_comparable_values_for_equality()


class VersionDto(ElementDto, Comparable):

    """Element Version
    """

    def __init__(self, version):
        """Class instantiation
        """
        super().__init__(version)

        self.uri = version.uri
        self.major = version.major
        self.minor = version.minor
        self.status = version.status

        self.types = {}
        self.methods = {}

    def get_comparable_values(self):
        """Return a tupple of values representing the unicity of the object
        """
        return (int(self.major), int(self.minor), str(self.name))


class CategoryDto(ElementDto, Comparable):

    """Element Category
    """

    def __init__(self, category):
        """Class instantiation
        """
        super().__init__(category)

        self.order = category.order

    def get_comparable_values(self):
        """Return a tupple of values representing the unicity of the object
        """
        return (int(self.order), str(self.name))


class TypeCategory(CategoryDto):

    """Element TypeCategory
    """

    def __init__(self, category):
        """Class instantiation
        """
        super().__init__(category)
        self.types = []

    def get_used_types(self):
        """Return list of types of the namspace used
        """
        used_types = RootDto.instance().get_used_types()
        for type in [y for (x, y) in self.types.items() if x not in used_types]:
            logging.getLogger().warn("Unused type %s" % type.name)
        return [y for (x, y) in self.types.items() if x in used_types]


class MethodCategory(CategoryDto):

    """Element MethodCategory
    """

    def __init__(self, category):
        """Class instantiation
        """
        super().__init__(category)
        self.methods = []


class MethodDto(ElementVersionedDto, Comparable):

    def __init__(self, method):
        """Class instantiation
        """
        super().__init__(method)

        self.method = method.method

        self.code = []
        self.full_uri = []
        self.absolute_uri = []

        self.changes_status = {}

        self.request_headers = []
        self.request_parameters = []
        self.request_body = []
        self.response_codes = []
        self.response_body = []

        self.originals = {}

    def get_comparable_values(self):
        """Return a tupple of values representing the unicity of the object
        """
        return (str(self.name))


class MultiVersion(Comparable):

    class Changes(Enum):
        """List of availables Change for this element
        """
        none = 1
        new = 2
        updated = 3
        deleted = 4

    def __init__(self, value, version):
        self.versions = [version]
        self.value = value

    def get_comparable_values(self):
        """Return a tupple of values representing the unicity of the object
        """
        return (self.value, sorted(self.versions))


class ParameterDto(ElementDto, Comparable):

    def __init__(self, parameter):
        """Class instantiation
        """
        super().__init__(parameter)
        self.type = parameter.type
        self.optional = parameter.optional
        self.is_internal = self.type in Object.Types

    def get_comparable_values(self):
        """Return a tupple of values representing the unicity of the object
        """
        return (str(self.name), str(self.description))


class PositionableParameterDto(ParameterDto):

    def __init__(self, parameter):
        """Class instantiation
        """
        super().__init__(parameter)
        self.position = 0

    def get_comparable_values_for_ordering(self):
        """Return a tupple of values representing the unicity of the object
        """
        return (int(self.position), str(self.name), str(self.description))


class ResponseCodeDto(ElementDto, Comparable):

    def __init__(self, parameter):
        """Class instantiation
        """
        super().__init__(parameter)
        self.code = parameter.code
        self.message = parameter.message

    def get_comparable_values(self):
        """Return a tupple of values representing the unicity of the object
        """
        return (int(self.code), str(self.message), str(self.description))


class TypeDto(ElementVersionedDto, Comparable):

    """Element Type
    """

    def __init__(self, type):
        """Class instantiation
        """
        super().__init__(type)

        self.name = type.name
        self.format = TypeFormatDto(type.format)

        self.changes_status = {}

        self.primary = []
        self.values = []

        self.originals = {}

    def get_comparable_values(self):
        """Return a tupple of values representing the unicity of the object
        """
        return (str(self.name))


class TypeFormatDto():

    """Element Type
    """

    def __init__(self, type_format):
        """Class instantiation
        """
        self.sample = []
        self.pretty = []
        self.advanced = []


class ObjectDto(ElementDto, Comparable):

    """Element Object
    """

    @classmethod
    def factory(cls, object_source):
        """Return a proper object
        """
        if object_source.type is Object.Types.object:
            return ObjectObjectDto(object_source)
        elif object_source.type not in Object.Types:
            return ObjectTypeDto(object_source)
        elif object_source.type is Object.Types.array:
            return ObjectArrayDto(object_source)
        else:
            return ObjectDto(object_source)

    def __init__(self, object):
        """Class instantiation
        """
        super().__init__(object)
        self.type = object.type
        self.optional = object.optional
        self.required = object.required

    def get_comparable_values(self):
        """Return a tupple of values representing the unicity of the object
        """
        return (str(self.name), str(self.description), str(self.type), bool(self.optional), bool(self.required))


class ObjectObjectDto(ObjectDto):

    """Element ObjectObject
    """

    def __init__(self, object):
        """Class instantiation
        """
        super().__init__(object)
        self.properties = {}


class ObjectArrayDto(ObjectDto):

    """Element ObjectObject
    """

    def __init__(self, object):
        """Class instantiation
        """
        super().__init__(object)
        self.items = None


class ObjectTypeDto(ObjectDto):

    """Element ObjectObject
    """

    def __init__(self, object):
        """Class instantiation
        """
        super().__init__(object)
        self.type_name = object.type_name
        self.primary = None
        self.values = []
