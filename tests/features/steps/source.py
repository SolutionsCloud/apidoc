from behave import given, when, then
import os
from apidoc.object.config import Config
from apidoc.factory.source import Source as SourceFactory


def assert_equals(first, second):
    assert first == second, "%s is not equals to %s" % (first, second)


def assert_in(needle, haystack):
    assert needle in haystack, "%s is not in to %s" % (needle, haystack)


def assert_notin(needle, haystack):
    assert needle not in haystack, "%s is not in to %s" % (needle, haystack)


@given('a "{format}" source file containing')
def given_source_file(context, format):
    name = os.path.join(context.temp_dir, "sample_source_%d.%s" % (len(context.conf_files), format))
    context.conf_files.append(name)

    f = open(name, "w")
    f.write(context.text)
    f.close()


@when('a source_factory load this file')
def when_factory_config(context):
    factory = SourceFactory()
    config = Config()
    config["input"]["files"] = context.conf_files
    response = factory.create_from_config(config)
    context.root = response


@then('the root contains "{count}" versions')
def then_count_versions(context, count):
    assert_equals(int(count), len(context.root.versions))


@then('the root contains "{count}" method\'s categories')
def then_count_method_categories(context, count):
    assert_equals(int(count), len(context.root.method_categories))


@then('the root contains "{count}" type\'s categories')
def then_count_type_categories(context, count):
    assert_equals(int(count), len(context.root.type_categories))


@then('the root contains "{count}" methods')
def then_count_methods(context, count):
    methods = dict((method.name, method) for category in context.root.method_categories for method in category.methods)
    assert_equals(int(count), len(methods))


@then('the root contains "{count}" types')
def then_count_types(context, count):
    types = dict((type.name, type) for category in context.root.type_categories for type in category.types)
    assert_equals(int(count), len(types))


@then('the changes status of method "{method}" is "{status}" for the version "{version}"')
def then_changes_status(context, method, status, version):
    methods = dict((method.name, method) for category in context.root.method_categories for method in category.methods)

    assert_equals(status, str(methods[method].changes_status[version]))


@then('the "{attribute}" of method "{method}" is "{value}" for the version "{version}"')
def then_attribute_value(context, attribute, method, value, version):
    methods = dict((method.name, method) for category in context.root.method_categories for method in category.methods)
    current_value = [x.value for x in getattr(methods[method], attribute) if version in x.versions][0]

    assert_equals(value, current_value)


@then('the "{attribute}" of method "{method}" contains a "{parameter}" for the version "{version}"')
def then_attribute_values(context, attribute, method, parameter, version):
    methods = dict((method.name, method) for category in context.root.method_categories for method in category.methods)
    current_values = dict((x.value.name, x.value) for x in getattr(methods[method], attribute) if version in x.versions)

    assert_in(parameter, current_values)


@then('the "{attribute}" of method "{method}" does not contains a "{parameter}" for the version "{version}"')
def then_not_attribute_values(context, attribute, method, parameter, version):
    methods = dict((method.name, method) for category in context.root.method_categories for method in category.methods)
    current_values = dict((x.value.name, x.value) for x in getattr(methods[method], attribute) if version in x.versions)

    assert_notin(parameter, current_values)


@then('the "{attribute}" of method "{method}" contains in order "{param1}" then "{param2}" for the version "{version}"')
def then_attribute_values_order(context, attribute, method, param1, param2, version):
    methods = dict((method.name, method) for category in context.root.method_categories for method in category.methods)
    current_values = [x.value.name for x in sorted(getattr(methods[method], attribute)) if version in x.versions]
    assert current_values.index(param1) < current_values.index(param2), "%s is not before %s in %s" % (param1, param2, current_values)


@then('the "{attribute}" of response_codes "{parameter}" of method "{method}" for the version "{version}" is "{value}"')
def then_parameter_attribute_values(context, attribute, parameter, method, version, value):
    methods = dict((method.name, method) for category in context.root.method_categories for method in category.methods)
    current_value = [x.value.message for x in methods[method].response_codes if version in x.versions and str(x.value.code) == parameter][0]

    assert_equals(current_value, value)
