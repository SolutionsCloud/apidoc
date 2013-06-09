from apidoc.object.source_raw import Object as ObjectRaw


class Type():

    def __init__(self, type_raw):
        self.name = type_raw.name
        self.sample = type_raw.format.sample
        self.pretty = type_raw.format.pretty
        self.advanced = type_raw.format.advanced


class Method():

    def __init__(self, method_raw):
        self.name = method_raw.name
        self.method = method_raw.method
        self.code = method_raw.code
        self.message = method_raw.message
        self.full_uri = method_raw.full_uri
        self.absolute_uri = method_raw.absolute_uri

        self.request_headers = [Parameter(x) for x in sorted(method_raw.request_headers.values())]
        self.request_parameters = dict((name, Parameter(x)) for name, x in method_raw.request_parameters.items())

        self.request_body = Object.factory(method_raw.request_body)
        self.response_body = Object.factory(method_raw.response_body)


class Parameter():

    def __init__(self, parameter_raw):
        self.name = parameter_raw.name
        self.optional = parameter_raw.optional
        self.sample = parameter_raw.get_sample()


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
        else:
            return Object(object_raw)

    def __init__(self, object_raw):
        self.name = object_raw.name
        self.type = object_raw.type
        self.optional = object_raw.optional
        self.sample = object_raw.get_sample()


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


class ObjectType(Object):

    def __init__(self, object_raw):
        super().__init__(object_raw)
