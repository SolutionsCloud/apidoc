from apidoc.object.source_raw import Object as ObjectRaw
from apidoc.object.source_raw import Constraintable
from apidoc.object import Comparable


class Type():

    def __init__(self, type_raw):
        self.name = type_raw.name
        self.sample = type_raw.get_sample()
        self.pretty = type_raw.format.pretty
        self.advanced = type_raw.format.advanced
        self.item = Object.factory(type_raw.item)


class Method(Comparable):

    def __init__(self, method_raw):
        self.name = method_raw.name
        self.method = method_raw.method
        self.code = method_raw.code
        self.message = method_raw.message
        self.full_uri = method_raw.full_uri
        self.absolute_uri = method_raw.absolute_uri

        self.request_headers = [Parameter(x) for x in method_raw.request_headers.values()]
        self.request_parameters = dict((name, Parameter(x)) for name, x in method_raw.request_parameters.items())

        self.request_body = Object.factory(method_raw.request_body)
        self.response_body = Object.factory(method_raw.response_body)

    def get_comparable_values(self):
        """Return a tupple of values representing the unicity of the object
        """
        return (str(self.name))


class Parameter(Comparable):

    def __init__(self, parameter_raw):
        self.name = parameter_raw.name
        self.optional = parameter_raw.optional
        self.sample = parameter_raw.get_sample()
        self.position = parameter_raw.position

    @property
    def is_query_string(self):
        return self.position < 0

    def get_comparable_values(self):
        """Return a tupple of values representing the unicity of the object
        """
        return (str(self.name), str(self.sample))


class Object():

    @classmethod
    def factory(cls, object_raw):
        """Return a proper object
        """
        if object_raw is None:
            return None
        if object_raw.type is ObjectRaw.Types.object:
            return ObjectObject(object_raw)
        elif object_raw.type is ObjectRaw.Types.type:
            return ObjectType(object_raw)
        elif object_raw.type is ObjectRaw.Types.array:
            return ObjectArray(object_raw)
        elif object_raw.type is ObjectRaw.Types.dynamic:
            return ObjectDynamic(object_raw)
        elif object_raw.type is ObjectRaw.Types.const:
            return ObjectConst(object_raw)
        elif object_raw.type is ObjectRaw.Types.enum:
            return ObjectEnum(object_raw)
        else:
            return Object(object_raw)

    def __init__(self, object_raw):
        self.name = object_raw.name
        self.type = object_raw.type
        self.optional = object_raw.optional
        self.sample = object_raw.get_sample()
        if isinstance(object_raw, Constraintable):
            self.constraints = object_raw.constraints
        else:
            self.constraints = {}


class ObjectObject(Object):

    def __init__(self, object_raw):
        super().__init__(object_raw)
        self.properties = dict((name, Object.factory(x)) for name, x in sorted(object_raw.properties.items()))


class ObjectArray(Object):

    def __init__(self, object_raw):
        super().__init__(object_raw)
        self.items = Object.factory(object_raw.items)
        self.sample_count = object_raw.sample_count


class ObjectDynamic(Object):

    def __init__(self, object_raw):
        super().__init__(object_raw)
        self.items = Object.factory(object_raw.items)


class ObjectConst(Object):

    def __init__(self, object_raw):
        super().__init__(object_raw)
        self.const_type = object_raw.const_type
        self.value = object_raw.value


class ObjectEnum(Object):

    def __init__(self, object_raw):
        super().__init__(object_raw)
        self.values = object_raw.values


class ObjectType(Object):

    def __init__(self, object_raw):
        super().__init__(object_raw)
        if object_raw.type_object is not None:
            self.type_object = Object.factory(object_raw.type_object.item)
