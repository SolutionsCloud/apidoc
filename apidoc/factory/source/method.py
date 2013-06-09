from apidoc.object.source_raw import Method as ObjectMethod

from apidoc.factory.source.element import Element as ElementFactory
from apidoc.factory.source.parameter import Parameter as ParameterFactory
from apidoc.factory.source.object import Object as ObjectFactory
from apidoc.factory.source.responseCode import ResponseCode as ResponseCodeFactory

from apidoc.lib.util.decorator import add_property


@add_property("parameter_factory", ParameterFactory)
@add_property("object_factory", ObjectFactory)
@add_property("response_code_factory", ResponseCodeFactory)
class Method(ElementFactory):
    """ Method Factory
    """

    def create_from_name_and_dictionary(self, name, datas):
        """Return a populated object Method from dictionary datas
        """
        method = ObjectMethod()
        self.set_common_datas(method, name, datas)
        if "category" in datas:
            method.category = str(datas["category"])
        if "code" in datas:
            method.code = int(datas["code"])
        if "uri" in datas:
            method.uri = str(datas["uri"])
        if "method" in datas:
            method.method = self.get_enum("method", ObjectMethod.Methods, datas)

        method.request_headers = self.parameter_factory.create_dictionary_of_element_from_dictionary("request_headers", datas)
        method.request_parameters = self.parameter_factory.create_dictionary_of_element_from_dictionary("request_parameters", datas)
        method.response_codes = self.response_code_factory.create_list_of_element_from_dictionary("response_codes", datas)

        if "request_body" in datas and datas["request_body"]:
            method.request_body = self.object_factory.create_from_name_and_dictionary("request", datas["request_body"])
        if "response_body" in datas and datas["response_body"]:
            method.response_body = self.object_factory.create_from_name_and_dictionary("response", datas["response_body"])
        return method
