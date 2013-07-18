import unittest

from apidoc.service.source import Source as SourceService
from apidoc.object.source_dto import Root


class TestSource(unittest.TestCase):

    def setUp(self):
        self.source = SourceService()

    def test_validate__nothing(self):
        with self.assertRaises(Exception):
            self.source.validate("foo")

    def test_validate(self):
        self.source.validate(Root())
