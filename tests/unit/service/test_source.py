import unittest

from apidoc.service.source import Source as SourceService
from apidoc.object.source_raw import Root, Version, Parameter, Method
from apidoc.object.source_dto import Root as RootDto
from apidoc.factory.source.rootDto import Hydrator


class TestSource(unittest.TestCase):

    def setUp(self):
        self.source = SourceService()

    def test_validate__nothing(self):
        with self.assertRaises(Exception):
            self.source.validate("foo")

    def test_validate(self):
        self.source.validate(RootDto())

    def test_get_uri_with_missing_parameters(self):
        root = Root()
        version = Version()
        version.name = "v"
        method = Method()
        method.name = "m"
        method.category = "a"
        method.full_uri = "/{foo}/{p}"

        parameter = Parameter()
        parameter.name = "p"
        parameter.type = "string"
        method.request_parameters = {"p": parameter}

        root.versions = {"v": version}
        version.methods = {"m": method}
        version.types = {"m": type}

        root_dto = RootDto()

        hydrator = Hydrator(version, {"v": version}, [])
        hydrator.hydrate_method(root_dto, root, method)

        parameters = self.source.validate(root_dto)
        parameters = self.source.get_uri_with_missing_parameters(root_dto)

        self.assertEqual([
            {"name": "foo", "uri": "/{foo}/{p}", "method": "m", "version": "v"},
        ], parameters)
