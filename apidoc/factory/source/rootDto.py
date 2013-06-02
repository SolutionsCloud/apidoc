from apidoc.object.source import RootDto as ObjectRoot
from apidoc.object.source import Category, VersionDto
from apidoc.object.source import MethodCategory, TypeCategory
from apidoc.object.source import MethodDto, TypeDto
from apidoc.object.source import MultiVersion
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

        #self.fix_versions(root)
        #self.refactor_hierarchy(root)

        from apidoc.lib.util.serialize import json_repr
        print(json_repr(rootDto))
        return rootDto

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
        else:
            method_dto = MethodDto(method)
            category.methods.append(method_dto)

        self.hydrate__attribute(method_dto.description, method.description, version.name)
        self.hydrate__attribute(method_dto.uri, method.uri, version.name)
        self.hydrate__attribute(method_dto.code, method.code, version.name)

    def hydrate__attribute(self, attribute, value, version):
        find = False
        for versioned_value in attribute:
            if versioned_value.value == value:
                versioned_value.versions.append(version)
                find = True

        if not find:
            attribute.append(MultiVersion(value, version))

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
        else:
            type_dto = TypeDto(type)
            category.types.append(type_dto)

        self.hydrate__attribute(type_dto.description, type.description, version.name)
        self.hydrate__attribute(type_dto.primary, type.primary, version.name)

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
