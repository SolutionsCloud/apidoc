import collections

from copy import deepcopy

from apidoc.object.source import Root, Sampleable, Displayable
from apidoc.object.source import Version, Configuration
from apidoc.object.source import Method, Type, MethodCategory, TypeCategory, Category
from apidoc.object.source import MethodCrossVersion, TypeCrossVersion, ElementCrossVersion
from apidoc.object.source import Parameter, ResponseCode
from apidoc.object.source import Type, EnumType, EnumTypeValue
from apidoc.object.source import Object, ObjectObject, ObjectArray
from apidoc.object.source import ObjectNumber, ObjectString, ObjectBool, ObjectNone
from apidoc.object.source import ObjectDynamic, ObjectReference, ObjectType
from apidoc.service.parser import Parser
from apidoc.service.merger import Merger
from apidoc.service.extender import Extender

from apidoc.lib.util.decorator import add_property
from apidoc.lib.util.cast import to_bool


@add_property("parser", Parser)
@add_property("merger", Merger)
@add_property("extender", Extender)
class Source():

    """Create source objet
    """

    def load_from_config(self, config):
        """Load a set of source's file defined in the config object and returned a populated ObjectRoot
        """
        sources = []
        if (config["input"]["directories"] is not None):
            for directory in config["input"]["directories"]:
                sources.extend(self.parser.load_all_from_directory(directory))
        if (config["input"]["files"] is not None):
            for file in config["input"]["files"]:
                sources.append(self.parser.load_from_file(file))

        merged = self.merger.merge_sources(sources)
        if config["input"]["arguments"] is not None:
            for (argument, value) in config["input"]["arguments"].items():
                merged = self.replace_argument(merged, argument, value)

        extended = self.extender.extends(
            merged, paths=self.get_extender_paths(), separator="/", extends_key="extends",
            inherit_key="inherit", removed_key="removed"
        )

        root = self.populate(extended)
        self.apply_config_filter(root, config["filter"])
        self.remove_undisplayed(root)
        self.fix_versions(root)
        self.refactor_hierarchy(root)

        return root

    def replace_argument(self, element, argument, value):
        """Replace sources arguments by value injected in config
        """
        if isinstance(element, list):
            return [self.replace_argument(x, argument, value) for x in element]
        elif isinstance(element, dict):
            return dict((x, self.replace_argument(y, argument, value)) for (x, y) in element.items())
        elif isinstance(element, str):
            return element.replace("${%s}" % argument, value)
        else:
            return element

    def apply_config_filter(self, root, config_filter):
        """Remove filter defined in config
        """
        if (config_filter["versions"]["includes"] is not None):
            for version in (version for version in root.versions.values() if version.name not in config_filter["versions"]["includes"]):
                version.display = False
        if (config_filter["versions"]["excludes"] is not None):
            for version in (version for version in root.versions.values() if version.name in config_filter["versions"]["excludes"]):
                version.display = False
        if (config_filter["categories"]["includes"] is not None):
            for category in (category for category in root.categories.values() if category.name not in config_filter["categories"]["includes"]):
                category.display = False
        if (config_filter["categories"]["excludes"] is not None):
            for category in (category for category in root.categories.values() if category.name in config_filter["categories"]["excludes"]):
                category.display = False

    def remove_undisplayed(self, root):
        """Remove elements marked a not to display
        """
        root.versions = dict((x, y) for x, y in root.versions.items() if y.display)
        displayed_categories = [category.name for category in root.categories.values() if category.display]
        for version in root.versions.values():
            version.methods = dict((x, y) for x, y in version.methods.items() if y.display and (y.category is None or y.category in displayed_categories))

    def fix_versions(self, root):
        """Set the version of elements
        """
        for (version_name, version) in root.versions.items():
            for (type_name, type) in version.types.items():
                type.version = version_name
            for (reference_name, reference) in version.references.items():
                reference.version = version_name
            for (method_name, method) in version.methods.items():
                method.version = version_name

    def refactor_hierarchy(self, root):
        """Modify elements structure (root/version/elements/) to (root/elementByVersion/element)
            Todo: This method is not solid
        """
        root.methods = {}
        root.method_categories = {}
        root.types = {}
        root.type_categories = {}
        root.references = {}
        for (version_name, version) in root.versions.items():
            for (reference_name, reference) in version.references.items():
                if reference_name not in root.references:
                    root.references[reference_name] = ElementCrossVersion(element=reference)
                root.references[reference_name].versions[version_name] = reference

            for (type_name, type) in version.types.items():
                if type.category not in root.type_categories:
                    root.type_categories[type.category] = TypeCategory(name=type.category)
                    if type.category in root.categories:
                        root.type_categories[type.category].order = root.categories[type.category].order
                        root.type_categories[type.category].description = root.categories[type.category].description

                if type_name not in root.type_categories[type.category].types:
                    root.type_categories[type.category].types[type_name] = TypeCrossVersion(element=type)
                root.type_categories[type.category].types[type_name].versions[version_name] = type

                if type.signature not in root.type_categories[type.category].types[type_name].signatures:
                    root.type_categories[type.category].types[type_name].signatures[type.signature] = type

                if type_name not in root.types:
                    root.types[type_name] = TypeCrossVersion(element=type)
                root.types[type_name].versions[version_name] = type

            for (method_name, method) in version.methods.items():
                if method.category not in root.method_categories:
                    root.method_categories[method.category] = MethodCategory(name=method.category)
                    if method.category in root.categories:
                        root.method_categories[method.category].order = root.categories[method.category].order
                        root.method_categories[method.category].description = root.categories[method.category].description

                if method_name not in root.method_categories[method.category].methods:
                    root.method_categories[method.category].methods[method_name] = MethodCrossVersion(element=method)
                root.method_categories[method.category].methods[method_name].versions[version_name] = method

                if method.signature not in root.method_categories[method.category].methods[method_name].signatures:
                    root.method_categories[method.category].methods[method_name].signatures[method.signature] = method

                if method_name not in root.methods:
                    root.methods[method_name] = MethodCrossVersion(element=method)
                root.methods[method_name].versions[version_name] = method

            del(version.methods)
            del(version.types)
            del(version.references)

    def get_extender_paths(self):
        """Retrieve extension lookup path
        """
        return (
            "categories/?",
            "versions/?",
            "versions/?/methods/?",
            "versions/?/types/?",
            "versions/?/references/?",
        )

    def get_enum(self, property, enum, datas):
        """Factory enum type
        """
        str_property = str(datas[property]).lower()
        if not str_property in enum:
            raise ValueError("Unknow enum \"%s\" for \"%s\"." % (str_property, property))
        return enum(str_property)

    def populate(self, datas):
        """Return a populated ObjectRoot from dictionnary datas
        """
        root = Root.instance()

        if "configuration" in datas and datas["configuration"] is not None:
            root.configuration = self.populate_configuration(datas["configuration"])
        if "categories" in datas and datas["categories"] is not None:
            root.categories = self.populate_list("categories", datas, self.populate_category)
        root.versions = self.populate_list("versions", datas, self.populate_version)

        return root

    def populate_element(self, element, name, datas):
        """Populated common data for an element from dictionnary datas
        """
        element.name = str(name)
        if "description" in datas:
            element.description = str(datas["description"]).strip()
        if isinstance(element, Sampleable) and element.sample is None and "sample" in datas:
            element.sample = str(datas["sample"]).strip()
        if isinstance(element, Displayable) and "display" in datas:
            element.display = to_bool(datas["display"])

    def populate_list(self, property_name, datas, callback):
        """Populate a list of elements
        """
        list = {}
        if property_name in datas and datas[property_name] is not None and isinstance(datas[property_name], collections.Iterable):
            for key, value in datas[property_name].items():
                list[key] = callback(key, value)
        return list

    def populate_configuration(self, datas):
        """Return a populated ObjectConfiguration from dictionnary datas
        """
        configuration = Configuration()

        if "uri" in datas:
            configuration.uri = str(datas["uri"])
        if "title" in datas:
            configuration.title = str(datas["title"])
        if "description" in datas:
            configuration.description = str(datas["description"])

        return configuration

    def populate_version(self, name, datas):
        """Return a populated ObjectVersion from dictionnary datas
        """
        version = Version()
        self.populate_element(version, name, datas)

        if "uri" in datas:
            version.uri = str(datas["uri"])
        if "major" in datas:
            version.major = int(datas["major"])
        if "minor" in datas:
            version.minor = int(datas["minor"])
        if "status" in datas:
            version.status = self.get_enum("status", Version.Status, datas)

        version.methods = self.populate_list("methods", datas, self.populate_method)
        version.types = self.populate_list("types", datas, self.populate_type)
        version.references = self.populate_list("references", datas, self.populate_object)

        return version

    def populate_category(self, name, datas):
        """Return a populated ObjectCategory from dictionnary datas
        """
        category = Category(name)
        self.populate_element(category, name, datas)

        if "order" in datas:
            category.order = int(datas["order"])

        return category

    def populate_method(self, name, datas):
        """Return a populated ObjectMethod from dictionnary datas
        """
        method = Method()
        self.populate_element(method, name, datas)
        if "category" in datas:
            method.category = str(datas["category"])
        else:
            method.category = None

        if "code" in datas:
            method.code = int(datas["code"])
        if "uri" in datas:
            method.uri = str(datas["uri"])
        if "method" in datas:
            method.method = self.get_enum("method", Method.Methods, datas)

        method.request_headers = self.populate_list("request_headers", datas, self.populate_parameter)
        method.request_parameters = self.populate_list("request_parameters", datas, self.populate_parameter)

        if "response_codes" in datas and datas["response_codes"] is not None and isinstance(datas["response_codes"], list):
            for value_code in datas["response_codes"]:
                method.response_codes.append(self.populate_response_code(value_code))

        if "request_body" in datas and datas["request_body"]:
            method.request_body = self.populate_object("request", datas["request_body"])

        if "response_body" in datas and datas["response_body"]:
            method.response_body = self.populate_object("request", datas["response_body"])

        return method

    def populate_parameter(self, name, datas):
        """Return a populated ObjectParameter from dictionnary datas
        """
        parameter = Parameter()
        self.populate_element(parameter, name, datas)

        if "optional" in datas:
            parameter.optional = to_bool(datas["optional"])

        if "type" in datas:
            parameter.type = str(datas["type"])

        return parameter

    def populate_response_code(self, datas):
        """Return a populated ObjectResponseCode from dictionnary datas
        """
        if "code" not in datas:
            raise ValueError("A response code must contain a code in \"%s\"." % repr(datas))

        code = ResponseCode()
        self.populate_element(code, datas["code"], datas)

        default_messages = {
            100: "Continue",
            101: "Switching Protocols",
            200: "OK",
            201: "Created",
            202: "Accepted",
            203: "Non-Authoritative Information",
            204: "No Content",
            205: "Reset Content",
            206: "Partial Content",
            300: "Multiple Choices",
            301: "Moved Permanently",
            302: "Found",
            303: "See Other",
            304: "Not Modified",
            305: "Use Proxy",
            307: "Temporary Redirect",
            400: "Bad Request",
            401: "Unauthorized",
            402: "Payment Required",
            403: "Forbidden",
            404: "Not Found",
            405: "Method Not Allowed",
            406: "Not Acceptable",
            407: "Proxy Authentication Required",
            408: "Request Time-out",
            409: "Conflict",
            410: "Gone",
            411: "Length Required",
            412: "Precondition Failed",
            413: "Request Entity Too Large",
            414: "Request-URI Too Large",
            415: "Unsupported Media Type",
            416: "Requested range not satisfiable",
            417: "Expectation Failed",
            500: "Internal Server Error",
            501: "Not Implemented",
            502: "Bad Gateway",
            503: "Service Unavailable",
            504: "Gateway Time-out",
            505: "HTTP Version not supported"
        }

        code.code = int(datas["code"])
        if "message" in datas:
            code.message = str(datas["message"])
        elif code.code in default_messages.keys():
            code.message = default_messages[code.code]

        return code

    def populate_type(self, name, datas):
        """Return a populated ObjectType from dictionnary datas
        """
        if "primary" in datas:
            primary = self.get_enum("primary", Type.Primaries, datas)
        else:
            raise ValueError("A type\'s primary must be set in type \"%s\"." % name)

        if primary is Type.Primaries.enum:
            type = EnumType()
        else:
            type = Type()

        type.primary = primary
        self.populate_element(type, name, datas)

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

        if isinstance(type, EnumType):
            type.values = self.populate_list("values", datas, self.populate_enum_type_value)

        return type

    def populate_enum_type_value(self, name, datas):
        """Return a populated ObjecyEnumTypeValue from dictionnary datas
        """
        enum_value = EnumTypeValue()
        self.populate_element(enum_value, name, datas)

        return enum_value

    def populate_object(self, name, datas):
        """Return a populated ObjectObject from dictionnary datas
        """
        if "type" not in datas:
            raise ValueError("Missing type in object \"%s\"  \"%s\"." % (name, repr(datas)))

        str_type = str(datas["type"]).lower()
        if not str_type in Object.Types:
            type = Object.Types("type")
        else:
            type = Object.Types(str_type)

        if type is Object.Types.object:
            object = ObjectObject()
            object.properties = self.populate_list("properties", datas, self.populate_object)
        elif type is Object.Types.array:
            object = ObjectArray()
            if "items" in datas:
                object.items = self.populate_object("items", datas["items"])
            if "sample_count" in datas:
                object.sample_count = int(datas["sample_count"])
        elif type is Object.Types.number:
            object = ObjectNumber()
        elif type is Object.Types.string:
            object = ObjectString()
        elif type is Object.Types.bool:
            object = ObjectBool()
            if "sample" in datas:
                object.sample = to_bool(datas["sample"])
        elif type is Object.Types.reference:
            object = ObjectReference()
            if "reference" in datas:
                object.reference_name = str(datas["reference"])
        elif type is Object.Types.type:
            object = ObjectType()
            object.type_name = str(datas["type"])
        elif type is Object.Types.none:
            object = ObjectNone()
        elif type is Object.Types.dynamic:
            object = ObjectDynamic()
            if "items" in datas:
                object.items = str(datas["items"])
            if "sample" in datas:
                if isinstance(datas["sample"], dict):
                    object.sample = {}
                    for k, v in datas["sample"].items():
                        object.sample[str(k)] = str(v)
                else:
                    raise ValueError("A dictionnary is expected for dynamic\s object in \"%s\"" % name)

        self.populate_element(object, name, datas)
        object.type = type
        if "optional" in datas:
            object.optional = to_bool(datas["optional"])
        if "required" in datas:
            object.required = to_bool(datas["required"])

        return object
