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

        for version in sorted(root_source.versions.values()):
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
                        item.changes_status[version.name] = MultiVersion.Changes.deleted
                        new = False
                    else:
                        item.changes_status[version.name] = MultiVersion.Changes.none
                else:
                    if not new:
                        item.changes_status[version.name] = MultiVersion.Changes.new
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
            method_dto.changes_status[self.version_name] = MultiVersion.Changes.none
        else:
            method_dto = MethodDto(method)
            category.methods.append(method_dto)
            method_dto.changes_status[self.version_name] = MultiVersion.Changes.new

        method_uri = "%s%s%s" % (root_source.configuration.uri or "", self.versions[self.version_name].uri or "", method.uri or "")
        parameters = [PositionableParameterDto(parameter) for parameter in method.request_parameters.values()]
        for parameter in parameters:
            parameter.position = method_uri.find("{%s}" % parameter.name)
        request_parameters = [parameter for parameter in parameters if parameter.position >= 0]
        request_headers = [ParameterDto(parameter) for parameter in method.request_headers.values()]
        response_codes = [ResponseCodeDto(parameter) for parameter in method.response_codes]

        changes = 0
        changes += self.hydrate_value(method_dto.description, method.description)
        changes += self.hydrate_value(method_dto.uri, method_uri)
        changes += self.hydrate_value(method_dto.code, method.code)

        changes += self.hydrate_list(method_dto.request_headers, sorted(request_headers))
        changes += self.hydrate_list(method_dto.request_parameters, sorted(request_parameters))
        changes += self.hydrate_list(method_dto.response_codes, sorted(response_codes))

        changes += self.hydrade_object(method_dto.request_body, method.request_body)
        changes += self.hydrade_object(method_dto.response_body, method.response_body)

        if changes > 0 and method_dto.changes_status[self.version_name] is MultiVersion.Changes.none:
            method_dto.changes_status[self.version_name] = MultiVersion.Changes.updated

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
            type_dto.changes_status[self.version_name] = MultiVersion.Changes.none
        else:
            type_dto = TypeDto(type)
            category.types.append(type_dto)
            type_dto.changes_status[self.version_name] = MultiVersion.Changes.new

        changes = 0
        changes += self.hydrate_value(type_dto.description, type.description)
        changes += self.hydrate_value(type_dto.primary, type.primary)
        changes += self.hydrate_value(type_dto.format.pretty, type.format.pretty)
        changes += self.hydrate_value(type_dto.format.advanced, type.format.advanced)
        changes += self.hydrate_value(type_dto.format.sample, type.format.sample)
        if (isinstance(type, EnumType)):
            changes += self.hydrate_list(type_dto.values, type.values.values())

        if changes > 0 and type_dto.changes_status[self.version_name] is MultiVersion.Changes.none:
            type_dto.changes_status[self.version_name] = MultiVersion.Changes.updated

    def hydrate_value(self, dto_value, source_value):
        if source_value is None:
            return 0

        changes = 0
        find = False
        for versioned_value in dto_value:
            if versioned_value.value == source_value:
                versioned_value.versions.append(self.version_name)
                find = True
                changes += 1 if self.has_changed(versioned_value) else 0

        if not find:
            dto_value.append(MultiVersion(source_value, self.version_name))
            return 1

        return changes

    def hydrate_list(self, dto_list, source_list):
        changes = 0
        for source_value in source_list:
            find = False
            for versioned_value in dto_list:
                if versioned_value.value == source_value:
                    versioned_value.versions.append(self.version_name)
                    find = True
                    changes += 1 if self.has_changed(versioned_value) else 0

            if not find:
                dto_list.append(MultiVersion(source_value, self.version_name))
                changes += 1

        return changes

    def hydrade_object(self, dto_object, source_object):
        if source_object is None:
            return 0

        if source_object.type is ObjectObject.Types.reference:
            reference = self.references[source_object.reference_name]
            return self.hydrade_object(dto_object, reference)

        source_dto = ObjectDto.factory(source_object)

        changes = 0
        find = None
        for versioned_value in dto_object:
            if versioned_value.value == source_dto:
                versioned_value.versions.append(self.version_name)
                find = versioned_value
                changes += 1 if self.has_changed(versioned_value) else 0

        if find is None:
            changes += 1
            if source_dto.type is ObjectObject.Types.object:
                for (property_name, property_value) in source_object.properties.items():
                    source_dto.properties[property_name] = []
                    changes += self.hydrade_object(source_dto.properties[property_name], property_value)
            elif source_dto.type is ObjectObject.Types.array:
                source_dto.items = []
                changes += self.hydrade_object(source_dto.items, source_object.items)
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
                        changes += self.hydrade_object(find.value.properties[property_name], property_value)
                    else:
                        changes += self.hydrade_object([], property_value)
            elif source_dto.type is ObjectObject.Types.array:
                changes += self.hydrade_object(find.value.items, source_object.items)

        return changes

    def has_changed(self, multi_version):
        previous_version = self.get_previous_version()
        if previous_version is None:
            return 0

        return previous_version not in multi_version.versions

    def get_previous_version(self):
        previsous = None
        for version in sorted(self.versions):
            if version == self.version_name:
                return previsous
            previsous = version

        raise ValueError("Unable to find current version in Version list")
