import unittest


from apidoc.factory.template import Template as TemplateFactory
from apidoc.service.template import Template as TemplateService
from apidoc.object.config import Config


class TestTemplate(unittest.TestCase):

    def setUp(self):
        self.template = TemplateFactory()

    def test_create_from_config(self):
        config = Config()

        response = self.template.create_from_config(config)

        self.assertIsInstance(response, TemplateService)
        self.assertEqual('default.html', response.input)
        self.assertEqual('stdout', response.output)
