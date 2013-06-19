from behave import given, when, then
import os
from apidoc.factory.config import Config as ConfigFactory


def assert_equals(first, second):
    assert first == second, "%s is not equals to %s" % (first, second)


@given('a "{format}" config file containing')
def given_config_file(context, format):
    context.conf_file = os.path.join(context.temp_dir, "sample." + format)

    f = open(context.conf_file, "w")
    f.write(context.text)
    f.close()


@when('a config_factory load this file')
def when_factory_config(context):
    factory = ConfigFactory()
    response = factory.load_from_file(context.conf_file)
    context.config_object = response


@then('the object_config returned contains "{text}" for the attribute "{attribute}"')
def then_text_attribute(context, text, attribute):
    part = context.config_object
    for a in attribute.split("."):
        part = part[a]
    assert_equals(str(part), text)


@then('the object_config returned contains the files "{text}" for the attribute "{attribute}"')
def then_files_attribute(context, text, attribute):
    part = context.config_object
    for a in attribute.split("."):
        part = part[a]

    text = text.replace("['", "['" + context.temp_dir + "/").replace(", '", ", '" + context.temp_dir + "/")
    assert_equals(str(part), text)


@then('the object_config returned contains the file "{text}" for the attribute "{attribute}"')
def the_file_attribute(context, text, attribute):
    part = context.config_object
    for a in attribute.split("."):
        part = part[a]

    text = context.temp_dir + "/" + text
    assert_equals(str(part), text)
