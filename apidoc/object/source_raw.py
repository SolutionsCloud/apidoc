from apidoc.lib.util.enum import Enum
from apidoc.object import Comparable


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


class Element():

    """Generic element
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.name = None
        self.description = None


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


class Constraintable():

    """Element who can provide constraints
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.constraints = {}


class Displayable():

    """Element who can be displayed
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.display = True
        self.label = ""


class Configuration(Element):

    """Element Configuration
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.uri = None
        self.title = None


class Version(Element, Displayable, Comparable):

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
        self.full_uri = None
        self.major = 1
        self.minor = 0
        self.status = Version.Status("current")
        self.methods = {}
        self.types = {}
        self.references = {}

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
        self.label = name
        self.order = 99


class Method(Element, Displayable, Comparable):

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
        option = 6
        patch = 7

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
        self.absolute_uri = None
        self.full_uri = None
        self.category = None
        self.method = Method.Methods("get")
        self.request_headers = {}
        self.request_parameters = {}
        self.request_body = None
        self.response_codes = []
        self.response_body = None

    def get_comparable_values(self):
        """Return a tupple of values representing the unicity of the object
        """
        return (str(self.name))


class Parameter(Element, Sampleable):

    """Element Parameter
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.type = None
        self.optional = False
        self.generic = False
        self.type_object = None
        self.position = 0

    def get_object(self):
        object = Object.factory(self.type, None)
        object.name = self.name
        return object

    def get_default_sample(self):
        """Return default value for the element
        """
        if self.type not in Object.Types or self.type is Object.Types.type:
            return self.type_object.get_sample()
        else:
            return self.get_object().get_sample()


class ResponseCode(Element):

    """Element ResponseCode
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.code = 200
        self.message = None
        self.generic = False


class Type(Element, Comparable, Sampleable):

    """Element Type
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.format = TypeFormat()
        self.category = None
        self.item = None

    def get_sample(self):
        """Return the a sample for the element
        """
        if self.item is not None:
            return self.item.get_sample()
        else:
            return super().get_sample()

    def get_comparable_values(self):
        """Return a tupple of values representing the unicity of the object
        """
        return (str(self.name))


class TypeFormat():

    """Element TypeFormat
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.pretty = None
        self.advanced = None


class Constraint(Comparable):

    """An oobject's constraint
    """

    def __init__(self, name, constraint):
        """Class instantiation
        """
        super().__init__()
        self.name = name
        self.constraint = constraint

    def __str__(self):
        return '%s: %s' % (self.name, str(self.constraint))

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

    def get_comparable_values(self):
        """Return a tupple of values representing the unicity of the object
        """
        return (str(self.name))


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
        boolean = 5
        none = 6
        reference = 7
        type = 8
        dynamic = 9
        const = 10
        enum = 11
        integer = 12

    @classmethod
    def factory(cls, str_type, version):
        """Return a proper object
        """
        type = Object.Types(str_type)

        if type is Object.Types.object:
            object = ObjectObject()
        elif type is Object.Types.array:
            object = ObjectArray()
        elif type is Object.Types.number:
            object = ObjectNumber()
        elif type is Object.Types.integer:
            object = ObjectInteger()
        elif type is Object.Types.string:
            object = ObjectString()
        elif type is Object.Types.boolean:
            object = ObjectBoolean()
        elif type is Object.Types.reference:
            object = ObjectReference()
        elif type is Object.Types.type:
            object = ObjectType()
        elif type is Object.Types.none:
            object = ObjectNone()
        elif type is Object.Types.dynamic:
            object = ObjectDynamic()
        elif type is Object.Types.const:
            object = ObjectConst()
        elif type is Object.Types.enum:
            object = ObjectEnum()
        else:
            object = Object()
        object.type = type
        object.version = version
        return object

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.type = None
        self.optional = False


class ObjectObject(Object, Constraintable):

    """Element ObjectObject
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.type = Object.Types("object")
        self.properties = {}


class ObjectArray(Object, Constraintable):

    """Element ObjectArray
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.type = Object.Types("array")
        self.items = None
        self.sample_count = 2


class ObjectNumber(Object, Constraintable):

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
        return '13.37'


class ObjectInteger(Object, Constraintable):

    """Element ObjectInteger
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.type = Object.Types("integer")

    def get_default_sample(self):
        """Return default value for the element
        """
        return '42'


class ObjectString(Object, Constraintable):

    """Element ObjectString
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.type = Object.Types("string")


class ObjectBoolean(Object, Constraintable):

    """Element ObjectBoolean
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.type = Object.Types("boolean")

    def get_default_sample(self):
        """Return default value for the element
        """
        return True


class ObjectNone(Object, Constraintable):

    """Element ObjectNone
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.type = Object.Types("none")


class ObjectDynamic(Object, Constraintable):

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


class ObjectConst(Object, Constraintable):

    """Element ObjectConst
    """

    class Types(Enum):

        """List of availables Primaries for this element
        """
        string = 1
        boolean = 2
        number = 3
        integer = 4

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.type = Object.Types("const")
        self.const_type = ObjectConst.Types.string
        self.value = None

    def get_default_sample(self):
        """Return default value for the element
        """
        return self.value


class ObjectEnum(Object, Constraintable):

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.type = Object.Types("enum")
        self.values = []
        self.descriptions = []

    def get_default_sample(self):
        """Return default value for the element
        """
        if not self.values:
            return super().get_default_sample()
        return self.values[0]


class EnumValue(Object, Comparable):

    def get_comparable_values(self):
        """Return a tupple of values representing the unicity of the object
        """
        return (str(self.name), str(self.description))


class ObjectReference(Object):

    """Element ObjectReference
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.type = Object.Types("reference")
        self.reference_name = None


class ObjectType(Object, Constraintable):

    """Element ObjectType
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.type = Object.Types("type")
        self.type_name = None
        self.type_object = None

    def get_default_sample(self):
        """Return default value for the element
        """
        if self.type_object is None:
            return super().get_default_sample()
        return self.type_object.get_sample()
