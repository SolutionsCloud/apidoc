from apidoc.object.source import RootDto as ObjectRoot
from apidoc.object.source import Category, VersionDto
from apidoc.object.source import MethodCategory, TypeCategory
from apidoc.object.source import MethodDto, TypeDto
from apidoc.object.source import MultiVersion, Element, EnumType
from apidoc.object.source import MethodCrossVersion, TypeCrossVersion, ElementCrossVersion


class RootDto():
    """ Root Factory
    """

    def create_from_root(self, root):
        """Return a populated Object Root from dictionnary datas
        """
        rootDto = ObjectRoot()

        rootDto.configuration = root.configuration
        rootDto.versions = [VersionDto(x) for x in root.versions.values()]

        for version in root.versions.values():
            for method in version.methods.values():
                self.hydrate_method(rootDto, root, method, version)
            for type in version.types.values():
                self.hydrate_type(rootDto, root, type, version)

        self.changed_status(rootDto)

        #self.fix_versions(root)
        #self.refactor_hierarchy(root)

        #TODO display only used types
        #TODO display only used categories

        from apidoc.lib.util.serialize import json_repr
        print(json_repr(rootDto))
        return rootDto

    def changed_status(self, rootDto):
        sorted_version = sorted(rootDto.versions)

        items = []
        for category in rootDto.method_categories:
            items = items + category.methods
        for category in rootDto.type_categories:
            items = items + category.types

        for item in items:
            new = False
            for version in sorted_version:
                if version.name not in item.changed_status.keys():
                    if new:
                        item.changed_status[version.name] = ElementCrossVersion.Change.deleted
                        new = False
                    else:
                        item.changed_status[version.name] = ElementCrossVersion.Change.none
                else:
                    if not new:
                        item.changed_status[version.name] = ElementCrossVersion.Change.new
                        new = True

    def hydrate_method(self, rootDto, root, method, version):
        categories = dict((category.name, category) for category in rootDto.method_categories)
        if method.category not in categories.keys():
            if method.category in root.categories.keys():
                category = MethodCategory(root.categories[method.category])
            else:
                category = MethodCategory(Category(method.category))
            rootDto.method_categories.append(category)
        else:
            category = categories[method.category]

        methods = dict((method.name, method) for method in category.methods)
        if method.name in methods.keys():
            method_dto = methods[method.name]
            method_dto.changed_status[version.name] = ElementCrossVersion.Change.none
        else:
            method_dto = MethodDto(method)
            category.methods.append(method_dto)
            method_dto.changed_status[version.name] = ElementCrossVersion.Change.new

        method_uri = "%s%s%s" % (root.configuration.uri or "", version.uri or "", method.uri or "")
        self.hydrate_value(method_dto.description, method.description, version.name)
        self.hydrate_value(method_dto.uri, method_uri, version.name)
        self.hydrate_value(method_dto.code, method.code, version.name)

        for parameter in method.request_parameters.values():
            parameter.position = method_uri.find("{%s}" % parameter.name)
        parameters = [parameter for parameter in method.request_parameters.values() if parameter.position >= 0]

        self.hydrate_list(method_dto.request_headers, sorted(method.request_headers.values()), version.name)
        self.hydrate_list(method_dto.request_parameters, sorted(parameters), version.name)
        self.hydrate_list(method_dto.response_codes, sorted(method.response_codes), version.name)

    def hydrate_type(self, rootDto, root, type, version):
        categories = dict((category.name, category) for category in rootDto.type_categories)
        if type.category not in categories.keys():
            if type.category in root.categories.keys():
                category = TypeCategory(root.categories[type.category])
            else:
                category = TypeCategory(Category(type.category))
            rootDto.type_categories.append(category)
        else:
            category = categories[type.category]

        types = dict((type.name, type) for type in category.types)
        if type.name in types.keys():
            type_dto = types[type.name]
            type_dto.changed_status[version.name] = ElementCrossVersion.Change.none
        else:
            type_dto = TypeDto(type)
            category.types.append(type_dto)
            type_dto.changed_status[version.name] = ElementCrossVersion.Change.new

        self.hydrate_value(type_dto.description, type.description, version.name)
        self.hydrate_value(type_dto.primary, type.primary, version.name)
        self.hydrate_value(type_dto.format.pretty, type.format.pretty, version.name)
        self.hydrate_value(type_dto.format.advanced, type.format.advanced, version.name)
        self.hydrate_value(type_dto.format.sample, type.format.sample, version.name)

        if (isinstance(type, EnumType)):
            self.hydrate_list(type_dto.values, type.values.values(), version.name)

    def equals(self, value1, value2):
        if isinstance(value1, Element):
            if isinstance(value2, Element):
                return value1.signature == value2.signature
            return False
        return value1 == value2

    def hydrate_value(self, dto_value, source_value, version):
        if source_value is None:
            return
        find = False
        for versioned_value in dto_value:
            if self.equals(versioned_value.value, source_value):
                versioned_value.versions.append(version)
                find = True

        if not find:
            dto_value.append(MultiVersion(source_value, version))

    def hydrate_list(self, dto_list, source_list, version):
        for source_value in source_list:
            find = False
            for versioned_value in dto_list:
                if self.equals(versioned_value.value.signature, source_value.signature):
                    versioned_value.versions.append(version)
                    find = True

            if not find:
                dto_list.append(MultiVersion(source_value, version))

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
