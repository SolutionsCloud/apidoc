from apidoc.object.source_dto import Root as ObjectRoot
from apidoc.object.source_raw import Category
from apidoc.object.source_raw import Object as ObjectRaw
from apidoc.object.source_dto import Version
from apidoc.object.source_dto import MethodCategory, TypeCategory
from apidoc.object.source_dto import Method, Type
from apidoc.object.source_dto import MultiVersion
from apidoc.object.source_dto import Parameter, RequestParameter, ResponseCode
from apidoc.object.source_dto import Object
from apidoc.object.source_sample import Type as TypeSample
from apidoc.object.source_sample import Method as MethodSample


class RootDto():
    """ Root Factory
    """

    def create_from_root(self, root_source):
        """Return a populated Object Root from dictionnary datas
        """

        root_dto = ObjectRoot()

        root_dto.configuration = root_source.configuration
        root_dto.versions = [Version(x) for x in root_source.versions.values()]

        for version in sorted(root_source.versions.values()):
            hydrator = Hydrator(version, root_source.versions, root_source.versions[version.name].types)
            for method in version.methods.values():
                hydrator.hydrate_method(root_dto, root_source, method)
            for type in version.types.values():
                hydrator.hydrate_type(root_dto, root_source, type)

        self.define_changes_status(root_dto)

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


class Hydrator():

    def __init__(self, version, versions, types):
        self.version_name = version.name
        self.versions = versions
        self.types = types

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
            method_dto = Method(method)
            category.methods.append(method_dto)
            method_dto.changes_status[self.version_name] = MultiVersion.Changes.new

        method_dto.versions.append(self.version_name)

        for parameter in method.request_parameters.values():
            parameter.position = method.full_uri.find("{%s}" % parameter.name)
        request_parameters = [RequestParameter(parameter) for parameter in method.request_parameters.values()]
        request_headers = [Parameter(parameter) for parameter in method.request_headers.values()]
        response_codes = [ResponseCode(parameter) for parameter in method.response_codes]

        changes = 0
        changes += self.hydrate_value(method_dto.description, method.description)
        changes += self.hydrate_value(method_dto.full_uri, method.full_uri)
        changes += self.hydrate_value(method_dto.absolute_uri, method.absolute_uri)
        changes += self.hydrate_value(method_dto.code, method.code)

        changes += self.hydrate_list(method_dto.request_headers, sorted(request_headers))
        changes += self.hydrate_list(method_dto.request_parameters, sorted(request_parameters))
        changes += self.hydrate_list(method_dto.response_codes, sorted(response_codes))

        changes += self.hydrate_object(method_dto.request_body, method.request_body)
        changes += self.hydrate_object(method_dto.response_body, method.response_body)

        if changes > 0 and method_dto.changes_status[self.version_name] is MultiVersion.Changes.none:
            method_dto.changes_status[self.version_name] = MultiVersion.Changes.updated

        method_dto.samples[self.version_name] = MethodSample(method)

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
            type_dto = Type(type)
            category.types.append(type_dto)
            type_dto.changes_status[self.version_name] = MultiVersion.Changes.new

        type_dto.versions.append(self.version_name)

        changes = 0
        changes += self.hydrate_value(type_dto.description, type.description)
        changes += self.hydrate_value(type_dto.format.pretty, type.format.pretty)
        changes += self.hydrate_value(type_dto.format.advanced, type.format.advanced)
        changes += self.hydrate_object(type_dto.item, type.item)

        if changes > 0 and type_dto.changes_status[self.version_name] is MultiVersion.Changes.none:
            type_dto.changes_status[self.version_name] = MultiVersion.Changes.updated

        type_dto.samples[self.version_name] = TypeSample(type)

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

    def hydrate_object(self, dto_object, source_object):
        if source_object is None:
            return 0

        source_dto = Object.factory(source_object)

        changes = 0
        find = None
        for versioned_value in dto_object:
            if versioned_value.value == source_dto:
                versioned_value.versions.append(self.version_name)
                find = versioned_value
                changes += 1 if self.has_changed(versioned_value) else 0

        if find is None:
            changes += 1
            if source_dto.type is ObjectRaw.Types.object:
                for (property_name, property_value) in source_object.properties.items():
                    source_dto.properties[property_name] = []
                    changes += self.hydrate_object(source_dto.properties[property_name], property_value)
            elif source_dto.type is ObjectRaw.Types.array:
                source_dto.items = []
                changes += self.hydrate_object(source_dto.items, source_object.items)
            elif source_dto.type is ObjectRaw.Types.dynamic:
                source_dto.items = []
                changes += self.hydrate_object(source_dto.items, source_object.items)
            elif source_dto.type is ObjectRaw.Types.enum:
                source_dto.values = []
                source_dto.descriptions = []
                self.hydrate_list(source_dto.values, sorted(source_object.values))
                self.hydrate_list(source_dto.descriptions, sorted(source_object.descriptions))
            elif source_dto.type is ObjectRaw.Types.type:
                source_dto.type_object = source_object.type_object

            dto_object.append(MultiVersion(source_dto, self.version_name))
        else:
            if source_dto.type is ObjectRaw.Types.object:
                for (property_name, property_value) in source_object.properties.items():
                    if find.value.type is ObjectRaw.Types.object and property_name in find.value.properties.keys():
                        changes += self.hydrate_object(find.value.properties[property_name], property_value)
                    else:
                        find.value.properties[property_name] = []
                        changes += self.hydrate_object(find.value.properties[property_name], property_value)
            elif source_dto.type is ObjectRaw.Types.array:
                changes += self.hydrate_object(find.value.items, source_object.items)
            elif source_dto.type is ObjectRaw.Types.dynamic:
                changes += self.hydrate_object(find.value.items, source_object.items)
            elif source_dto.type is ObjectRaw.Types.enum:
                changes += self.hydrate_list(find.value.values, source_object.values)
                changes += self.hydrate_list(find.value.descriptions, source_object.descriptions)

        return changes

    def has_changed(self, multi_version):
        previous_version = self.get_previous_version()
        if previous_version is None:
            return False

        return previous_version.name not in multi_version.versions

    def get_previous_version(self):
        previous = None
        for version in sorted(self.versions.values()):
            if version.name == self.version_name:
                return previous
            previous = version

        raise ValueError("Unable to find current version in Version list")
