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

    def create_from_root(self, root_source):
        """Return a populated Object Root from dictionnary datas
        """
        root_dto = ObjectRoot()

        root_dto.configuration = root_source.configuration
        root_dto.versions = [VersionDto(x) for x in root_source.versions.values()]

        for version in root_source.versions.values():
            hydratator = Hydradator(version, root_source.versions, root_source.versions[version.name].types, root_source.versions[version.name].references)
            for method in version.methods.values():
                hydratator.hydrate_method(root_dto, root_source, method)
            for type in version.types.values():
                hydratator.hydrate_type(root_dto, root_source, type)

        self.define_changes_status(root_dto)

        #TODO display only used types
        #TODO display only used categories

        from apidoc.lib.util.serialize import json_repr
        print(json_repr(root_dto))

        return root_dto

    def define_changes_status(self, root_dto):
        sorted_version = sorted(root_dto.versions)

        items = []
        for category in root_dto.method_categories:
            items = items + category.methods
        for category in root_dto.type_categories:
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


class Hydradator():

    def __init__(self, version, versions, types, references):
        self.version_name = version.name
        self.versions = versions
        self.types = types
        self.references = references

    def hydrate_method(self, root_dto, root_source, method):
        categories = dict((category.name, category) for category in root_dto.method_categories)
        if method.category not in categories.keys():
            if method.category in root_source.categories.keys():
                category = MethodCategory(root_source.categories[method.category])
            else:
                category = MethodCategory(Category(method.category))
            root_dto.method_categories.append(category)
        else:
            category = categories[method.category]

        methods = dict((method.name, method) for method in category.methods)
        if method.name in methods.keys():
            method_dto = methods[method.name]
            method_dto.changes_status[self.version_name] = MultiVersion.Change.none
        else:
            method_dto = MethodDto(method)
            category.methods.append(method_dto)
            method_dto.changes_status[self.version_name] = MultiVersion.Change.new

        method_uri = "%s%s%s" % (root_source.configuration.uri or "", self.versions[self.version_name].uri or "", method.uri or "")
        self.hydrate_value(method_dto.description, method.description)
        self.hydrate_value(method_dto.uri, method_uri)
        self.hydrate_value(method_dto.code, method.code)

        parameters = [PositionableParameterDto(parameter) for parameter in method.request_parameters.values()]
        for parameter in parameters:
            parameter.position = method_uri.find("{%s}" % parameter.name)
        request_parameters = [parameter for parameter in parameters if parameter.position >= 0]
        request_headers = [ParameterDto(parameter) for parameter in method.request_headers.values()]
        response_codes = [ResponseCodeDto(parameter) for parameter in method.response_codes]

        self.hydrate_list(method_dto.request_headers, sorted(request_headers))
        self.hydrate_list(method_dto.request_parameters, sorted(request_parameters))
        self.hydrate_list(method_dto.response_codes, sorted(response_codes))

        self.hydrade_object(method_dto.request_body, method.request_body)
        self.hydrade_object(method_dto.response_body, method.response_body)

    def hydrate_type(self, root_dto, root, type):
        categories = dict((category.name, category) for category in root_dto.type_categories)
        if type.category not in categories.keys():
            if type.category in root.categories.keys():
                category = TypeCategory(root.categories[type.category])
            else:
                category = TypeCategory(Category(type.category))
            root_dto.type_categories.append(category)
        else:
            category = categories[type.category]

        types = dict((type.name, type) for type in category.types)
        if type.name in types.keys():
            type_dto = types[type.name]
            type_dto.changes_status[self.version_name] = MultiVersion.Change.none
        else:
            type_dto = TypeDto(type)
            category.types.append(type_dto)
            type_dto.changes_status[self.version_name] = MultiVersion.Change.new

        self.hydrate_value(type_dto.description, type.description)
        self.hydrate_value(type_dto.primary, type.primary)
        self.hydrate_value(type_dto.format.pretty, type.format.pretty)
        self.hydrate_value(type_dto.format.advanced, type.format.advanced)
        self.hydrate_value(type_dto.format.sample, type.format.sample)

        if (isinstance(type, EnumType)):
            self.hydrate_list(type_dto.values, type.values.values())

    def hydrate_value(self, dto_value, source_value):
        if source_value is None:
            return

        find = False
        for versioned_value in dto_value:
            if versioned_value.value == source_value:
                versioned_value.versions.append(self.version_name)
                find = True

        if not find:
            dto_value.append(MultiVersion(source_value, self.version_name))

    def hydrate_list(self, dto_list, source_list):
        for source_value in source_list:
            find = False
            for versioned_value in dto_list:
                if versioned_value.value == source_value:
                    versioned_value.versions.append(self.version_name)
                    find = True

            if not find:
                dto_list.append(MultiVersion(source_value, self.version_name))

    def hydrade_object(self, dto_object, source_object):
        if source_object is None:
            return None

        if source_object.type is ObjectObject.Types.reference:
            reference = self.references[source_object.reference_name]
            return self.hydrade_object(dto_object, reference)

        source_dto = ObjectDto.factory(source_object)

        find = None
        for versioned_value in dto_object:
            if versioned_value.value == source_dto:
                versioned_value.versions.append(self.version_name)
                find = versioned_value

        if find is None:
            if source_dto.type is ObjectObject.Types.object:
                for (property_name, property_value) in source_object.properties.items():
                    source_dto.properties[property_name] = self.hydrade_object([], property_value)
            elif source_dto.type is ObjectObject.Types.array:
                source_dto.items = self.hydrade_object([], source_object.items)
            elif source_dto.type is ObjectObject.Types.type:
                type = self.types[source_object.type_name]
                source_dto.primary = type.primary
                if isinstance(type, EnumType):
                    source_dto.values = [x for x in type.values.keys()]

            dto_object.append(MultiVersion(source_dto, self.version_name))
        else:
            if source_dto.type is ObjectObject.Types.object:
                for (property_name, property_value) in source_object.properties.items():
                    if find.value.type is ObjectObject.Types.object and property_name in find.value.properties.keys():
                        find.value.properties[property_name] = self.hydrade_object(find.value.properties[property_name], property_value)
                    else:
                        find.value.properties[property_name] = self.hydrade_object([], property_value)
            elif source_dto.type is ObjectObject.Types.array:
                source_dto.items = self.hydrade_object(find.value.items, source_object.items)

        return dto_object
