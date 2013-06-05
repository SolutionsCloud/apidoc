from apidoc.object.source import RootDto as ObjectRoot
from apidoc.object.source import Category, VersionDto
from apidoc.object.source import MethodCategory, TypeCategory
from apidoc.object.source import MethodDto, TypeDto
from apidoc.object.source import MultiVersion, EnumType
from apidoc.object.source import ObjectObject
from apidoc.object.source import ParameterDto, PositionableParameterDto, ResponseCodeDto
from apidoc.object.source import ObjectDto


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

        self.define_changes_status(rootDto)

        #TODO display only used types
        #TODO display only used categories
        #TODO inject type data into ObjectType (needed for signature)
        #TODO inject reference data into ObjectReference

        from apidoc.lib.util.serialize import json_repr
        print(json_repr(rootDto))

        return rootDto

    def define_changes_status(self, rootDto):
        sorted_version = sorted(rootDto.versions)

        items = []
        for category in rootDto.method_categories:
            items = items + category.methods
        for category in rootDto.type_categories:
            items = items + category.types

        for item in items:
            new = False
            for version in sorted_version:
                if version.name not in item.changes_status.keys():
                    if new:
                        item.changes_status[version.name] = MultiVersion.Change.deleted
                        new = False
                    else:
                        item.changes_status[version.name] = MultiVersion.Change.none
                else:
                    if not new:
                        item.changes_status[version.name] = MultiVersion.Change.new
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
            method_dto.changes_status[version.name] = MultiVersion.Change.none
        else:
            method_dto = MethodDto(method)
            category.methods.append(method_dto)
            method_dto.changes_status[version.name] = MultiVersion.Change.new

        method_uri = "%s%s%s" % (root.configuration.uri or "", version.uri or "", method.uri or "")
        self.hydrate_value(method_dto.description, method.description, version.name)
        self.hydrate_value(method_dto.uri, method_uri, version.name)
        self.hydrate_value(method_dto.code, method.code, version.name)

        parameters = [PositionableParameterDto(parameter) for parameter in method.request_parameters.values()]
        for parameter in parameters:
            parameter.position = method_uri.find("{%s}" % parameter.name)
        request_parameters = [parameter for parameter in parameters if parameter.position >= 0]
        request_headers = [ParameterDto(parameter) for parameter in method.request_headers.values()]
        response_codes = [ResponseCodeDto(parameter) for parameter in method.response_codes]

        self.hydrate_list(method_dto.request_headers, sorted(request_headers), version.name)
        self.hydrate_list(method_dto.request_parameters, sorted(request_parameters), version.name)
        self.hydrate_list(method_dto.response_codes, sorted(response_codes), version.name)

        self.hydrade_object(method_dto.request_body, method.request_body, version.name)
        self.hydrade_object(method_dto.response_body, method.response_body, version.name)

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
            type_dto.changes_status[version.name] = MultiVersion.Change.none
        else:
            type_dto = TypeDto(type)
            category.types.append(type_dto)
            type_dto.changes_status[version.name] = MultiVersion.Change.new

        self.hydrate_value(type_dto.description, type.description, version.name)
        self.hydrate_value(type_dto.primary, type.primary, version.name)
        self.hydrate_value(type_dto.format.pretty, type.format.pretty, version.name)
        self.hydrate_value(type_dto.format.advanced, type.format.advanced, version.name)
        self.hydrate_value(type_dto.format.sample, type.format.sample, version.name)

        if (isinstance(type, EnumType)):
            self.hydrate_list(type_dto.values, type.values.values(), version.name)

    def hydrate_value(self, dto_value, source_value, version):
        if source_value is None:
            return
        find = False
        for versioned_value in dto_value:
            if versioned_value.value == source_value:
                versioned_value.versions.append(version)
                find = True

        if not find:
            dto_value.append(MultiVersion(source_value, version))

    def hydrate_list(self, dto_list, source_list, version):
        for source_value in source_list:
            find = False
            for versioned_value in dto_list:
                if versioned_value.value == source_value:
                    versioned_value.versions.append(version)
                    find = True

            if not find:
                dto_list.append(MultiVersion(source_value, version))

    def hydrade_object(self, dto_object, source_object, version):
        if source_object is None:
            return None

        source_dto = ObjectDto.factory(source_object)

        find = None
        for versioned_value in dto_object:
            if versioned_value.value == source_dto:
                versioned_value.versions.append(version)
                find = versioned_value

        if find is None:
            if source_dto.type is ObjectObject.Types.object:
                for (property_name, property_value) in source_object.properties.items():
                    source_dto.properties[property_name] = self.hydrade_object([], property_value, version)

            dto_object.append(MultiVersion(source_dto, version))
        else:
            if source_dto.type is ObjectObject.Types.object:
                for (property_name, property_value) in source_object.properties.items():
                    if find.value.type is ObjectObject.Types.object and property_name in find.value.properties.keys():
                        find.value.properties[property_name] = self.hydrade_object(find.value.properties[property_name], property_value, version)
                    else:
                        find.value.properties[property_name] = self.hydrade_object([], property_value, version)

        return dto_object
