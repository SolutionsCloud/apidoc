import hashlib
import logging

from functools import total_ordering, lru_cache
from apidoc.lib.util.enum import Enum
from apidoc.lib.util.tools import merge_dict


class Root():

    """Root object of sources elements
    """

    _instance = None

    @classmethod
    def instance(cls):
        """Retrieve the unique instance of the element
        """
        if Root._instance is None:
            Root._instance = Root()
        return Root._instance

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.configuration = Configuration()
        self.versions = {}
        self.sections = {}
        self.namespaces = {}
        self.types = {}
        self.references = {}

    @lru_cache()
    def previous_version(self, version):
        """return version previous to that provided in parameter
        """
        last_version = None
        for v in sorted(self.versions.values()):
            if v.name == version:
                return last_version
            last_version = v.name

        raise ValueError("Unknown version \"%s\"" % version)

    @lru_cache()
    def get_used_namespaces(self):
        """return list of used namespaces
        """
        for namespace in [x for x in self.namespaces.values() if len(x.get_used_types()) == 0]:
            logging.getLogger().warn("Unused namespace %s" % namespace.name)
        return [x for x in self.namespaces.values() if len(x.get_used_types()) > 0]

    @lru_cache()
    def get_used_types(self):
        """return list of types used in a method
        """
        types = []
        for section in self.sections.values():
            for method_versioned in section.methods.values():
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

    _signature = None
    _version = None

    def version():
        """The version property.
        """
        def fget(self):
            return self._version

        def fset(self, value):
            self._version = value

        return locals()
    version = property(**version())

    @property
    def signature(self):
        """Return a uniq signature of the element
        """
        if self._signature is None:
            self._signature = hashlib.md5(repr(self.get_signature_struct()).encode("UTF-8")).hexdigest()
        return self._signature

    def get_signature_struct(self):
        """Return a uniq signature of the element as dict
        """
        return {
            "name": self.name,
            "description": self.description
        }


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
class Sortable():

    """Element who can be sorted
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.name = None
        self.description = None

    def __lt__(self, other):
        """Return true if self is lower than other
        """
        return (str(self.name), str(self.description)) < (str(other.name), str(self.description))

    def __eq__(self, other):
        """Return true if self is equals to other
        """
        return (str(self.name), str(self.description)) == (str(other.name), str(self.description))


class Displayable():

    """Element who can be displayed
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.display = True

    def get_signature_struct(self):
        """Return a uniq signature of the element as dict
        """
        return {
            "display": self.display
        }


class Configuration(Element):

    """Element Configuration
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.uri = None
        self.title = None


class Version(Element, Sortable, Displayable):

    """Element Version
    """

    class Status(Enum):

        """List of availables Status for this element
        """
        current = 1
        beta = 2
        deprecated = 3
        draft = 4

    _full_uri = None

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.uri = None
        self.major = 1
        self.minor = 0
        self.status = Version.Status("current")
        self.sections = {}
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


    @property
    def full_uri(self):
        """Return full uri for the method
        """
        if self._full_uri is None:
            if Root.instance().configuration.uri is not None:
                self._full_uri = Root.instance().configuration.uri
                if self.uri is not None:
                    self._full_uri = "%s%s" % (Root.instance().configuration.uri, self.uri)
                else:
                    self._full_uri = Root.instance().configuration.uri
            elif self.uri is None:
                raise ValueError("No uri defined in version \"%s\"." % self.name)
            else:
                self._full_uri = self.uri
        return self._full_uri


class Section(Element, Sortable, Displayable):

    """Element Section
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.methods = {}
        self.order = 99

    @Element.version.setter
    def version(self, value):
        """Set the version and propagate it to is subelements
        """
        self._version = value
        for method in self.methods.values():
            method.version = value

    def __lt__(self, other):
        """Return true if self is lower than other
        """
        return (self.order, self.name) < (other.order, other.name)

    def __eq__(self, other):
        """Return true if self is equals to other
        """
        return (self.order, self.name) == (other.order, other.name)


class Method(Element, Sortable):

    """Element Section
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

    _full_uri = None

    @Element.version.setter
    def version(self, value):
        """Set the version and propagate it to is subelements
        """
        self._version = value
        for parameter in self.request_parameters.values():
            parameter.version = value
        for parameter in self.request_headers.values():
            parameter.version = value
        for parameter in self.response_codes:
            parameter.version = value
        if self.request_body:
            self.request_body.version = value
        if self.response_body:
            self.response_body.version = value

    def get_signature_struct(self):
        """Return a uniq signature of the element as dict
        """
        return merge_dict(super().get_signature_struct(), {
            "code": self.code,
            "uri": self.uri,
            "method": str(self.method),
            "request_headers": sorted([x.signature for x in self.request_headers.values()]),
            "request_parameters": sorted([x.signature for x in self.cleaned_request_parameters.values()]),
            "request_body": None if self.request_body is None else self.request_body.signature,
            "response_codes": sorted([x.signature for x in self.response_codes]),
            "response_body": None if self.response_body is None else self.response_body.signature,
        })

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

    @property
    def full_uri(self):
        """Return full uri for the method
        """
        if self._full_uri is None:
            self._full_uri = "%s%s" % (Root.instance().versions[self.version].full_uri, self.uri)
        return self._full_uri

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.code = 200
        self.uri = None
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


class Parameter(Element, Sampleable, Sortable):

    """Element Parameter
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.type = None
        self.optional = False
        self.position = 0

    def __lt__(self, other):
        """Return true if self is lower than other
        """
        return (int(self.position), str(self.name), str(self.description)) < (int(other.position), str(other.name), str(other.description))

    def __eq__(self, other):
        """Return true if self is equals to other
        """
        return (int(self.position), str(self.name), str(self.description)) == (int(other.position), str(other.name), str(other.description))

    def get_signature_struct(self):
        """Return a uniq signature of the element as dict
        """
        return merge_dict(super().get_signature_struct(), {
            "type": self.type,
            "position": self.position,
            "description": self.description,
            "optional": self.optional,
        })

    def get_object(self):
        object =  Object.factory(self.type, self.version)
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


class ResponseCode(Element, Sortable):

    """Element ResponseCode
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.code = 200
        self.message = None

    def __lt__(self, other):
        """Return true if self is lower than other
        """
        return (int(self.code), str(self.message), str(self.description)) < (int(other.code), str(other.message), str(self.description))

    def __eq__(self, other):
        """Return true if self is equals to other
        """
        return (int(self.code), str(self.message), str(self.description)) == (int(other.code), str(other.message), str(self.description))

    def get_signature_struct(self):
        """Return a uniq signature of the element as dict
        """
        return merge_dict(super().get_signature_struct(), {
            "code": self.code,
            "message": self.message,
        })


class Namespace(Element, Sortable):

    """Element Namespace
    """

    def __init__(self, name):
        """Class instantiation
        """
        super().__init__()
        self.name = name
        self.types = {}

    def get_used_types(self):
        """Return list of types of the namspace used
        """
        used_types = Root.instance().get_used_types();
        for type in [y for (x, y) in self.types.items() if x not in used_types]:
            logging.getLogger().warn("Unused type %s" % type.name)
        return [y for (x, y) in self.types.items() if x in used_types]


class Type(Element, Sortable):

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
        self.namespace = None

    def get_signature_struct(self):
        """Return a uniq signature of the element as dict
        """
        return merge_dict(super().get_signature_struct(), {
            "primary": self.primary,
            "format": self.format.get_signature_struct(),
        })


class TypeFormat(Sampleable):

    """Element TypeFormat
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.pretty = None
        self.advanced = None

    def get_signature_struct(self):
        """Return a uniq signature of the element as dict
        """
        return {
            "pretty": self.pretty,
            "advanced": self.advanced,
        }

    def get_default_sample(self):
        """Return default value for the element
        """
        if self.pretty is not None:
            return self.pretty

        return super().get_default_sample()


class EnumType(Type):

    """Element EnumType
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.primary = Type.Primaries.enum
        self.values = {}

    def get_signature_struct(self):
        """Return a uniq signature of the element as dict
        """
        return merge_dict(super().get_signature_struct(), {
            "values": sorted([x.signature for x in self.values.values()])
        })


class EnumTypeValue(Element, Sortable):

    """Element EnumTypeValue
    """

    pass


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

    _unit_signature = None

    def get_signature_struct(self):
        """Return a uniq signature of the element as dict
        """
        return merge_dict(super().get_signature_struct(), {
            "type": str(self.type),
            "optional": self.optional,
            "required": self.required,
        })

    @property
    def unit_signature(self):
        """Return a uniq signature of the element
        """
        if self._unit_signature is None:
            self._unit_signature = hashlib.md5(repr(self.get_unit_signature_struct()).encode("UTF-8")).hexdigest()
        return self._unit_signature

    def get_unit_signature_struct(self):
        """Return a uniq signature of the element as dict
        """
        return {
            "description": str(self.description),
            "type": str(self.type),
            "optional": self.optional,
            "required": self.required,
        }

    def get_used_types(self):
        """Return list of types used in the object
        """
        return []


class ObjectObject(Object):

    """Element ObjectObject
    """

    def __init__(self):
        """Class instantiation
        """
        super().__init__()
        self.type = Object.Types("object")
        self.properties = {}

    @Element.version.setter
    def version(self, value):
        """Set the version and propagate it to is subelements
        """
        self._version = value
        for object in self.properties.values():
            object.version = value

    def get_signature_struct(self):
        """Return a uniq signature of the element as dict
        """
        return merge_dict(super().get_signature_struct(), {
            "properties": sorted([x.signature for x in self.properties.values()])
        })

    def get_unit_signature_struct(self):
        """Return a uniq signature of the element as dict
        """
        return super().get_unit_signature_struct()

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

    @Element.version.setter
    def version(self, value):
        """Set the version and propagate it to is subelements
        """
        self._version = value
        if self.items is not None:
            self.items.version = value

    def get_signature_struct(self):
        """Return a uniq signature of the element as dict
        """
        return merge_dict(super().get_signature_struct(), {
            "items": None if self.items is None else self.items.signature
        })

    def get_unit_signature_struct(self):
        """Return a uniq signature of the element as dict
        """
        return super().get_unit_signature_struct()

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

    def get_signature_struct(self):
        """Return a uniq signature of the element as dict
        """
        return merge_dict(super().get_signature_struct(), {
            "items": self.items
        })

    def get_unit_signature_struct(self):
        """Return a uniq signature of the element as dict
        """
        return super().get_unit_signature_struct()

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

    def get_signature_struct(self):
        """Return a uniq signature of the element as dict
        """
        return merge_dict(super().get_signature_struct(), {
            "reference": self.get_reference().signature
        })

    def get_unit_signature_struct(self):
        """Return a uniq signature of the element as dict
        """
        return super().get_unit_signature_struct()

    def get_reference(self):
        """Return a reference object from the reference_name defined in sources
        """
        if self.reference_name not in Root.instance().references:
            raise ValueError(
                "Unable to find reference \"%s\"." % self.reference_name
            )
        if self.version not in Root.instance().references[self.reference_name].versions:
            raise ValueError(
                "Unable to find reference \"%s\" at version \"%s\"." % (self.reference_name, self.version)
            )

        return Root.instance().references[self.reference_name].versions[self.version]

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

    def get_signature_struct(self):
        """Return a uniq signature of the element as dict
        """
        return merge_dict(super().get_signature_struct(), {
            "type": self.get_type().signature
        })

    def get_unit_signature_struct(self):
        """Return a uniq signature of the element as dict
        """
        return self.get_signature_struct()

    def get_type(self):
        """Return a type object from the type_name defined in sources
        """
        if self.type_name not in Root.instance().types:
            raise ValueError("Unable to find type \"%s\"." % self.type_name)
        if self.version not in Root.instance().types[self.type_name].versions:
            raise ValueError("Unable to find type \"%s\" at version \"%s\"." % (self.type_name, self.version))

        return Root.instance().types[self.type_name].versions[self.version]

    def get_default_sample(self):
        """Return default value for the element
        """
        return self.get_type().format.get_sample()

    def get_used_types(self):
        """Return list of types used in the object
        """
        return [self.type_name]


class MergedMethod():

    def __init__(self):
        """Class instantiation
        """
        self.description = []
        self.full_uri = []
        self.request_parameters = []
        self.request_headers = []
        self.request_body = []
        self.response_body = []
        self.response_codes = []

class MergedType():

    def __init__(self):
        """Class instantiation
        """
        self.description = []
        self.primary = []
        self.values = []


class ElementCrossVersion(Element, Sortable):
    """Element ElementCrossVersion
    """

    class Change(Enum):
        """List of availables Change for this element
        """
        none = 1
        new = 2
        updated = 3
        deleted = 4

    _merged = None

    def __init__(self, element):
        """Class instantiation
        """
        super().__init__()
        self.name = element.name
        self.description = element.description
        self.reference = element
        self.versions = {}
        self.signatures = {}

    def changed_status(self, version):
        """Return the change status for the specified version
        """
        previous_version = Root.instance().previous_version(version)
        if previous_version is None:
            if version not in self.versions:
                return ElementCrossVersion.Change.none
            return ElementCrossVersion.Change.new

        if previous_version not in self.versions:
            if version not in self.versions:
                return ElementCrossVersion.Change.none
            return ElementCrossVersion.Change.new

        if version not in self.versions:
            return ElementCrossVersion.Change.deleted

        if self.versions[previous_version].signature != self.versions[version].signature:
            return ElementCrossVersion.Change.updated

        return ElementCrossVersion.Change.none


class TypeCrossVersion(ElementCrossVersion):

    @property
    def merged(self):
        """Return a merged reference
        """
        if self._merged is None:
            merged = MergedType()
            seen_values = []
            for m in self.versions.values():
                if m.description is not None and m.description not in merged.description:
                    merged.description.append(m.description)
                if m.primary is not None and m.primary not in merged.primary:
                    merged.primary.append(m.primary)
                if m.primary == Type.Primaries.enum:
                    for parameter in m.values.values():
                        if parameter.signature not in seen_values:
                            seen_values.append(parameter.signature)
                            merged.values.append(parameter)
            self._merged = merged
        return self._merged

class MethodCrossVersion(ElementCrossVersion):

    @property
    def merged(self):
        """Return a merged reference
        """
        if self._merged is None:
            merged = MergedMethod()
            seen_request_parameters = []
            seen_request_headers = []
            seen_response_codes = []
            for m in self.versions.values():
                if m.description is not None and m.description not in merged.description:
                    merged.description.append(m.description)
                if m.full_uri is not None and m.full_uri not in merged.full_uri:
                    merged.full_uri.append(m.full_uri)
                for parameter in m.cleaned_request_parameters.values():
                    if parameter.signature not in seen_request_parameters:
                        seen_request_parameters.append(parameter.signature)
                        merged.request_parameters.append(parameter)
                for parameter in m.request_headers.values():
                    if parameter.signature not in seen_request_headers:
                        seen_request_headers.append(parameter.signature)
                        merged.request_headers.append(parameter)
                for parameter in m.response_codes:
                    if parameter.signature not in seen_response_codes:
                        seen_response_codes.append(parameter.signature)
                        merged.response_codes.append(parameter)
                if m.request_body is not None:
                    merged.request_body.append(m.request_body)
                if m.response_body is not None:
                    merged.response_body.append(m.response_body)
            self._merged = merged
        return self._merged

    def objects_without_reference(self, objects):
        list_objects = []
        for object in objects:
            while object.type == Object.Types.reference:
                object = object.get_reference()
            list_objects.append(object)
        return list_objects

    def objects_by_unit_signature(self, objects):
        seen_signatures = []
        list_objects = []
        for object in self.objects_without_reference(objects):
            object.versions = [object.version]
            if object.unit_signature not in seen_signatures:
                seen_signatures.append(object.unit_signature)
                list_objects.append(object)
            else:
                for x in [x for x in list_objects if x.unit_signature == object.unit_signature]:
                    x.versions.append(object.version)
        return list_objects;

    def objects_merge_properties(self, objects):
        seen_signatures = []
        list_properties = {}
        for object in self.objects_without_reference(objects):
            if object.type == Object.Types.object:
                for (property_name, property_value) in object.properties.items():
                    if property_name not in list_properties.keys():
                        list_properties[property_name] = property_value
        return list_properties;

    def objects_property_by_property_name(self, objects, property_name):
        list_objects = []
        for object in [x for x in self.objects_without_reference(objects) if x.type is Object.Types.object]:
            if property_name in object.properties.keys():
                list_objects.append(object.properties[property_name])
        return list_objects;

    def objects_items(self, objects):
        list_objects = []
        for object in [x for x in self.objects_without_reference(objects) if x.type is Object.Types.array]:
            list_objects.append(object.items)
        return list_objects;

    def objects_reference(self, objects):
        list_objects = []
        for object in [x for x in objects if x.type is Object.Types.reference]:
            list_objects.append(object.get_reference())
        return list_objects;
