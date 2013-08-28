from apidoc.lib.util.enum import Enum
from apidoc.object.source_raw import Object as ObjectRaw
from apidoc.object.source_raw import Constraintable
from apidoc.object import Comparable


class Root():

    """Root object of sources elements for templates
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.configuration = None
        self.versions = []
        self.method_categories = []
        self.type_categories = []


class Element():

    """Element
    """

    def __init__(self, element):
        """Class instantiation
        """
        self.name = element.name
        self.description = element.description


class ElementVersioned():

    """Element
    """

    def __init__(self, element):
        """Class instantiation
        """
        self.name = element.name
        self.description = []


class Version(Element, Comparable):

    """Element Version
    """

    def __init__(self, version):
        """Class instantiation
        """
        super().__init__(version)
        self.label = version.label
        self.uri = version.uri
        self.major = version.major
        self.minor = version.minor
        self.status = version.status

    def get_comparable_values(self):
        """Return a tupple of values representing the unicity of the object
        """
        return (int(self.major), int(self.minor), str(self.label), str(self.name))


class Category(Element, Comparable):

    """Element Category
    """

    def __init__(self, category):
        """Class instantiation
        """
        super().__init__(category)

        self.label = category.label
        self.order = category.order

    def get_comparable_values(self):
        """Return a tupple of values representing the unicity of the object
        """
        return (int(self.order), str(self.label), str(self.name))


class TypeCategory(Category):

    """Element TypeCategory
    """

    def __init__(self, category):
        """Class instantiation
        """
        super().__init__(category)
        self.types = []


class MethodCategory(Category):

    """Element MethodCategory
    """

    def __init__(self, category):
        """Class instantiation
        """
        super().__init__(category)
        self.methods = []


class Method(ElementVersioned, Comparable):

    def __init__(self, method):
        """Class instantiation
        """
        super().__init__(method)

        self.label = method.label
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

        self.versions = []

        self.samples = {}

    @property
    def request_uri_parameters(self):
        return [x for x in self.request_parameters if not x.value.is_query_string]

    @property
    def request_query_string_parameters(self):
        return [x for x in self.request_parameters if x.value.is_query_string]

    def get_comparable_values(self):
        """Return a tupple of values representing the unicity of the object
        """
        return (str(self.label), str(self.name))


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


class Parameter(Element, Comparable):

    def __init__(self, parameter):
        """Class instantiation
        """
        super().__init__(parameter)
        self.type = parameter.type
        self.optional = parameter.optional
        self.generic = parameter.generic
        self.is_internal = self.type in ObjectRaw.Types or self.type is ObjectRaw.Types.type

    def get_comparable_values(self):
        """Return a tupple of values representing the unicity of the object
        """
        return (not self.generic, str(self.name), str(self.description))


class RequestParameter(Parameter):

    def __init__(self, parameter):
        """Class instantiation
        """
        super().__init__(parameter)
        self.position = parameter.position

    @property
    def is_query_string(self):
        return self.position < 0

    def get_comparable_values(self):
        """Return a tupple of values representing the unicity of the object
        """
        return (0 if self.position >= 0 else 1, not self.generic, str(self.name), str(self.description))

    def get_comparable_values_for_ordering(self):
        """Return a tupple of values representing the unicity of the object
        """

        return (0 if self.position >= 0 else 1, int(self.position), str(self.name), str(self.description))


class ResponseCode(Element, Comparable):

    def __init__(self, parameter):
        """Class instantiation
        """
        super().__init__(parameter)
        self.code = parameter.code
        self.message = parameter.message
        self.generic = parameter.generic

    def get_comparable_values(self):
        """Return a tupple of values representing the unicity of the object
        """
        return (not self.generic, int(self.code), str(self.message), str(self.description))


class Type(ElementVersioned, Comparable):

    """Element Type
    """

    def __init__(self, type):
        """Class instantiation
        """
        super().__init__(type)

        self.name = type.name
        self.format = TypeFormat(type.format)

        self.changes_status = {}

        self.item = []

        self.versions = []

        self.samples = {}

    def get_comparable_values(self):
        """Return a tupple of values representing the unicity of the object
        """
        return (str(self.name))


class TypeFormat():

    """Element Type
    """

    def __init__(self, type_format):
        """Class instantiation
        """
        self.sample = []
        self.pretty = []
        self.advanced = []


class Object(Element, Comparable):

    """Element Object
    """

    @classmethod
    def factory(cls, object_source):
        """Return a proper object
        """
        if object_source.type is ObjectRaw.Types.object:
            return ObjectObject(object_source)
        elif object_source.type not in ObjectRaw.Types or object_source.type is ObjectRaw.Types.type:
            return ObjectType(object_source)
        elif object_source.type is ObjectRaw.Types.array:
            return ObjectArray(object_source)
        elif object_source.type is ObjectRaw.Types.dynamic:
            return ObjectDynamic(object_source)
        elif object_source.type is ObjectRaw.Types.const:
            return ObjectConst(object_source)
        elif object_source.type is ObjectRaw.Types.enum:
            return ObjectEnum(object_source)
        else:
            return Object(object_source)

    def __init__(self, object):
        """Class instantiation
        """
        super().__init__(object)
        self.type = object.type
        self.optional = object.optional

        if isinstance(object, Constraintable):
            self.constraints = object.constraints

    def get_comparable_values(self):
        """Return a tupple of values representing the unicity of the object
        """
        return (str(self.name), str(self.description), str(self.type), bool(self.optional), str(self.constraints) if isinstance(self, Constraintable) else "")


class ObjectObject(Object):

    """Element ObjectObject
    """

    def __init__(self, object):
        """Class instantiation
        """
        super().__init__(object)
        self.properties = {}


class ObjectArray(Object):

    """Element ObjectArray
    """

    def __init__(self, object):
        """Class instantiation
        """
        super().__init__(object)
        self.items = None


class ObjectDynamic(Object):

    """Element ObjectDynamic
    """

    def __init__(self, object):
        """Class instantiation
        """
        super().__init__(object)
        self.items = None


class ObjectConst(Object):

    """Element ObjectConst
    """

    def __init__(self, object):
        """Class instantiation
        """
        super().__init__(object)
        self.const_type = object.const_type
        self.value = object.value


class ObjectEnum(Object):

    """Element ObjectEnum
    """

    def __init__(self, object):
        """Class instantiation
        """
        super().__init__(object)
        self.values = []
        self.descriptions = []

    def get_comparable_values(self):
        """Return a tupple of values representing the unicity of the object
        """
        return (str(self.name), str(self.description), str(self.constraints))


class EnumValue(Object):
    """Element ObjectEnum
    """

    def __init__(self, object):
        """Class instantiation
        """
        super().__init__(object)


class ObjectType(Object):

    """Element ObjectType
    """

    def __init__(self, object):
        """Class instantiation
        """
        super().__init__(object)
        self.type_name = object.type_name
        self.values = []
