import logging

from functools import total_ordering
from apidoc.lib.util.enum import Enum


class Root():

    """Root object of sources elements
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.configuration = Configuration()
        self.versions = {}
        self.categories = {}
        self.methods = {}
        self.types = {}
        self.references = {}


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
        self.configuration = Configuration()
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


class Element():

    """Generic element
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.name = None
        self.description = None


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


class Sampleable():

    """Element who can provide samples
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.sample = None

    def get_sample(self):
        """Return the a sample for the element
        """
        if self.sample is None:
            return self.get_default_sample()
        return self.sample

    def get_default_sample(self):
        """Return default value for the element
        """
        return "my_%s" % self.name


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


class Displayable():

    """Element who can be displayed
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.display = True


class Configuration(Element):

    """Element Configuration
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.uri = None
        self.title = None


class Version(Element, Displayable):

    """Element Version
    """

    class Status(Enum):

        """List of availables Status for this element
        """
        current = 1
        beta = 2
        deprecated = 3
        draft = 4

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.uri = None
        self.major = 1
        self.minor = 0
        self.status = Version.Status("current")
        self.methods = {}
        self.types = {}
        self.references = {}

    def __lt__(self, other):
        """Return true if self is lower than other
        """
        return (self.major, self.minor, self.name) < (other.major, other.minor, self.name)

    def __eq__(self, other):
        """Return true if self is equals to other
        """
        return (self.major, self.minor, self.name) == (other.major, other.minor, self.name)


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

    def get_comparable_values(self):
        """Return a tupple of values representing the unicity of the object
        """
        return (int(self.major), int(self.minor), str(self.name))


class Category(Element, Displayable):

    """Element Category
    """

    def __init__(self, name):
        """Class instantiation
        """
        super().__init__()
        self.name = name
        self.order = 99


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


class Method(Element, Displayable):

    """Element Method
    """

    class Methods(Enum):

        """List of availables Methods for this element
        """
        get = 1
        post = 2
        put = 3
        delete = 4
        head = 5
        http = 6

    @property
    def message(self):
        """Return default message for this element
        """
        if self.code != 200:
            for code in self.response_codes:
                if code.code == self.code:
                    return code.message

            raise ValueError("Unknown response code \"%s\" in \"%s\"." % (self.code, self.name))

        return "OK"

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.code = 200
        self.uri = None
        self.category = None
        self.method = Method.Methods("get")
        self.request_headers = {}
        self.request_parameters = {}
        self.request_body = None
        self.response_codes = []
        self.response_body = None

    @property
    def cleaned_request_parameters(self):
        """Remove parameter who are not definied in uri
        """
        for parameter in self.request_parameters.values():
            parameter.position = self.uri.find("{%s}" % parameter.name)
        return dict((x, y) for x, y in self.request_parameters.items() if y.position >= 0)

    def get_used_types(self):
        """Return list of types used in the method
        """
        types = []
        for param in self.request_headers.values():
            types += param.get_used_types()
        for param in self.cleaned_request_parameters.values():
            types += param.get_used_types()
        if self.request_body is not None:
            types += self.request_body.get_used_types()
        if self.response_body is not None:
            types += self.response_body.get_used_types()

        return list({}.fromkeys(types).keys())


class MethodDto(ElementVersionedDto, Comparable):

    def __init__(self, method):
        """Class instantiation
        """
        super().__init__(method)

        self.method = method.method

        self.code = []
        self.uri = []

        self.changes_status = {}

        self.request_headers = []
        self.request_parameters = []
        self.request_body = []
        self.response_codes = []
        self.response_body = []

    def get_comparable_values(self):
        """Return a tupple of values representing the unicity of the object
        """
        return (str(self.name))


class MultiVersion(Comparable):

    class Change(Enum):
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


class ParameterDto(ElementDto, Sampleable, Comparable):

    def __init__(self, parameter):
        """Class instantiation
        """
        super().__init__(parameter)
        self.type = parameter.type
        self.optional = parameter.optional

    def get_comparable_values(self):
        """Return a tupple of values representing the unicity of the object
        """
        return (str(self.name), str(self.description))

    def get_object(self):
        object = Object.factory(self.type, None)
        object.name = self.name
        return object


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


class Parameter(Element, Sampleable):

    """Element Parameter
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.type = None
        self.optional = False

    def get_object(self):
        object = Object.factory(self.type, None)
        object.name = self.name
        return object

    def get_default_sample(self):
        """Return default value for the element
        """
        return self.get_object().get_sample()

    def get_used_types(self):
        """Return list of types used in the parameter
        """
        return [self.type]


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


class ResponseCode(Element):

    """Element ResponseCode
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.code = 200
        self.message = None


class Type(Element):

    """Element Type
    """

    class Primaries(Enum):

        """List of availables Primaries for this element
        """
        string = 1
        enum = 2
        number = 3

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.primary = Type.Primaries.string
        self.format = TypeFormat()
        self.category = None

    def get_sample(self):
        """Return the a sample for the element
        """
        if self.format.sample is None:
            return self.get_default_sample()
        return self.format.sample

    def get_default_sample(self):
        """Return default value for the element
        """
        return "my_%s" % self.name


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

    def get_comparable_values(self):
        """Return a tupple of values representing the unicity of the object
        """
        return (str(self.name))


class TypeFormat(Sampleable):

    """Element TypeFormat
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.pretty = None
        self.advanced = None

    def get_default_sample(self):
        """Return default value for the element
        """
        if self.pretty is not None:
            return self.pretty

        return None


class TypeFormatDto(Sampleable):

    """Element Type
    """

    def __init__(self, type_format):
        """Class instantiation
        """
        self.sample = []
        self.pretty = []
        self.advanced = []


class EnumType(Type):

    """Element EnumType
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.primary = Type.Primaries.enum
        self.values = {}

    def get_default_sample(self):
        """Return default value for the element
        """
        if len(self.values) > 0:
            return [x for x in self.values.keys()][0]
        return super().get_default_sample()


class EnumTypeValue(Element, Comparable):

    """Element EnumTypeValue
    """

    def get_comparable_values(self):
        """Return a tupple of values representing the unicity of the object
        """
        return (str(self.name), str(self.description))


class ObjectDto(ElementDto, Comparable):

    """Element Object
    """

    @classmethod
    def factory(cls, object_source):
        """Return a proper object
        """
        if isinstance(object_source, ObjectObject):
            return ObjectObjectDto(object_source)
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


class Object(Element, Sampleable):

    """Element Object
    """

    class Types(Enum):

        """List of availables Types for this element
        """
        object = 1
        array = 2
        number = 3
        string = 4
        bool = 5
        none = 6
        reference = 7
        type = 8
        dynamic = 9

    @classmethod
    def factory(cls, str_type, version):
        """Return a proper object
        """
        if str_type in Object.Types:
            type = Object.Types(str_type)

            if type is Object.Types.object:
                object = ObjectObject()
            elif type is Object.Types.array:
                object = ObjectArray()
            elif type is Object.Types.number:
                object = ObjectNumber()
            elif type is Object.Types.string:
                object = ObjectString()
            elif type is Object.Types.bool:
                object = ObjectBool()
            elif type is Object.Types.reference:
                object = ObjectReference()
            elif type is Object.Types.type:
                object = ObjectType()
            elif type is Object.Types.none:
                object = ObjectNone()
            elif type is Object.Types.dynamic:
                object = ObjectDynamic()
            object.type = type
        else:
            object = ObjectType()
            object.type = Object.Types("type")
            object.type_name = str_type

        object.version = version
        return object

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.type = None
        self.optional = False
        self.required = True

    def get_used_types(self):
        """Return list of types used in the object
        """
        return []


class ObjectObjectDto(ObjectDto):

    """Element ObjectObject
    """

    def __init__(self, object):
        """Class instantiation
        """
        super().__init__(object)
        self.properties = {}


class ObjectObject(Object):

    """Element ObjectObject
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.type = Object.Types("object")
        self.properties = {}

    def get_used_types(self):
        """Return list of types used in the object
        """
        types = []
        for element in self.properties.values():
            types += element.get_used_types()
        return types


class ObjectArray(Object):

    """Element ObjectArray
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.type = Object.Types("array")
        self.items = None
        self.sample_count = 2

    def get_used_types(self):
        """Return list of types used in the object
        """
        if self.items is not None:
            return self.items.get_used_types()
        return []


class ObjectNumber(Object):

    """Element ObjectNumber
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.type = Object.Types("number")

    def get_default_sample(self):
        """Return default value for the element
        """
        return '123'


class ObjectString(Object):

    """Element ObjectString
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.type = Object.Types("string")


class ObjectBool(Object):

    """Element ObjectBool
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.type = Object.Types("bool")

    def get_default_sample(self):
        """Return default value for the element
        """
        return 'true'


class ObjectNone(Object):

    """Element ObjectNone
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.type = Object.Types("none")


class ObjectDynamic(Object):

    """Element ObjectDynamic
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.type = Object.Types("dynamic")
        self.items = None

    def get_default_sample(self):
        """Return default value for the element
        """
        return {
            "key1": "my_%s" % self.name,
            "key2": "sample"
        }

    def get_used_types(self):
        """Return list of types used in the object
        """
        return [self.items]


class ObjectReference(Object):

    """Element ObjectReference
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.type = Object.Types("reference")
        self.reference_name = None

    def get_reference(self):
        """Return a reference object from the reference_name defined in sources
        """
        if self.reference_name not in RootDto.instance().references:
            print(RootDto.instance().references.keys())
            raise ValueError(
                "Unable to find reference \"%s\"." % self.reference_name
            )
        if self.version not in RootDto.instance().references[self.reference_name].versions:
            raise ValueError(
                "Unable to find reference \"%s\" at version \"%s\"." % (self.reference_name, self.version)
            )

        reference = RootDto.instance().references[self.reference_name].versions[self.version]
        if self.optional:
            reference.optional = self.optional
        if self.description is not None:
            reference.description = self.description
        return reference

    def get_used_types(self):
        """Return list of types used in the object
        """
        return self.get_reference().get_used_types()


class ObjectType(Object):

    """Element ObjectType
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.type = Object.Types("type")
        self.type_name = None

    def get_type(self):
        """Return a type object from the type_name defined in sources
        """
        return Type()
        if self.type_name not in RootDto.instance().types:
            raise ValueError("Unable to find type \"%s\"." % self.type_name)
        if self.version not in RootDto.instance().types[self.type_name].versions:
            raise ValueError("Unable to find type \"%s\" at version \"%s\"." % (self.type_name, self.version))

        return RootDto.instance().types[self.type_name].versions[self.version]

    def get_default_sample(self):
        """Return default value for the element
        """
        return self.get_type().format.get_sample()

    def get_used_types(self):
        """Return list of types used in the object
        """
        return [self.type_name]
