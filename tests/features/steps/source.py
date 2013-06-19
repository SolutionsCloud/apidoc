from behave import given, when, then
import os
from apidoc.object.config import Config
from apidoc.factory.source import Source as SourceFactory


def assert_equals(first, second):
    assert first == second, "%s is not equals to %s" % (first, second)


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
    methods = []
    for category in context.root.method_categories:
        methods += category.methods
    assert_equals(int(count), len(methods))


@then('the root contains "{count}" types')
def then_count_types(context, count):
    types = []
    for category in context.root.type_categories:
        types += category.types
    assert_equals(int(count), len(types))
