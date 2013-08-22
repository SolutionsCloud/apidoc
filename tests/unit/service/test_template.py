import unittest
import tempfile
import os
from io import StringIO

from apidoc.service.template import Template as TemplateService
from apidoc.object.source_dto import Root
from apidoc.object.config import Config

from jinja2 import Environment, FileSystemLoader


class Testtemplate(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.template = TemplateService()

        self.template.output = "default"
        template_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '..',
            '..',
            '..',
            'apidoc',
            'template',
            'default.html'
        )
        self.template.input = os.path.basename(template_file)
        self.template.env = Environment(loader=FileSystemLoader(os.path.dirname(template_file)))

    def test_render__folder(self):
        source = Root()
        config = Config()
        config["output"]["componants"] = "local"

        template_dir = self.template.env.loader.searchpath[0]
        if os.path.exists(os.path.join(template_dir, "resource", "js", "combined.js")):
            os.remove(os.path.join(template_dir, "resource", "js", "combined.js"))

        self.template.output = os.path.join(self.temp_dir, "index.html")
        self.template.render(source, config)

        files = [f for f in os.listdir(os.path.join(self.temp_dir))]
        self.assertIn("index.html", files)
        self.assertIn("font", files)
        self.assertIn("css", files)
        self.assertIn("js", files)

    def test_render__remote(self):
        source = Root()
        config = Config()
        config["output"]["componants"] = "remote"

        template_dir = self.template.env.loader.searchpath[0]
        if os.path.exists(os.path.join(template_dir, "resource", "js", "combined.js")):
            os.remove(os.path.join(template_dir, "resource", "js", "combined.js"))

        self.template.output = os.path.join(self.temp_dir, "foo", "index.html")
        self.template.render(source, config)

        files = [f for f in os.listdir(os.path.join(self.temp_dir, "foo"))]
        self.assertIn("index.html", files)
        self.assertIn("font", files)
        self.assertIn("css", files)
        self.assertIn("js", files)
        files_js = [f for f in os.listdir(os.path.join(self.temp_dir, "foo", "js"))]
        self.assertNotIn("jquery.min.js", files_js)

    def test_render__output(self):
        source = Root()
        config = Config()

        self.template.output = "stdout"

        out = StringIO()
        self.template.render(source, config, out=out)
        output = out.getvalue().strip()

        files = [f for f in os.listdir(self.temp_dir)]
        self.assertEqual(0, len(files))
        self.assertNotEqual(0, len(output))

    def test_render__template(self):
        source = Root()
        config = Config()
        config["output"]["template"] = __file__

        self.template.output = os.path.join(self.temp_dir, "index.html")
        self.template.render(source, config)

        files = [f for f in os.listdir(os.path.join(self.temp_dir))]
        self.assertIn("index.html", files)
        self.assertNotIn("font", files)
        self.assertNotIn("css", files)
        self.assertNotIn("js", files)
