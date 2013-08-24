import os
import shutil
import sys
import logging


class Template():

    """Provide tool to managed templates
    """

    def __init__(self):
        """Class instantiation
        """
        self.input = "default.html"
        self.output = "stdout"
        self.env = None

    def render(self, sources, config, out=sys.stdout):
        """Render the documentation as defined in config Object
        """
        template = self.env.get_template(self.input)
        output = template.render(sources=sources, layout=config["output"]["layout"], config=config["output"])
        if self.output == "stdout":
            out.write(output)
        else:
            dir = os.path.dirname(self.output)
            if not os.path.exists(dir):
                os.makedirs(dir)
            if config["output"]["template"] == "default":
                if config["output"]["componants"] == "local":
                    for template_dir in self.env.loader.searchpath:
                        files = (
                            os.path.join(template_dir, "resource", "js", "combined.js"),
                            os.path.join(template_dir, "resource", "css", "combined.css"),
                            os.path.join(template_dir, "resource", "font", "apidoc.eot"),
                            os.path.join(template_dir, "resource", "font", "apidoc.woff"),
                            os.path.join(template_dir, "resource", "font", "apidoc.ttf"),
                            os.path.join(template_dir, "resource", "font", "source-code-pro.eot"),
                            os.path.join(template_dir, "resource", "font", "source-code-pro.woff"),
                            os.path.join(template_dir, "resource", "font", "source-code-pro.ttf"),
                        )

                        for file in files:
                            filename = os.path.basename(file)
                            dirname = os.path.basename(os.path.dirname(file))

                            if not os.path.exists(os.path.join(dir, dirname)):
                                os.makedirs(os.path.join(dir, dirname))
                            if os.path.exists(file):
                                shutil.copyfile(file, os.path.join(dir, dirname, filename))
                            else:
                                logging.getLogger().warn('Missing resource file "%s". If you run apidoc in virtualenv, run "%s"' % (filename, "python setup.py resources"))

                if config["output"]["componants"] == "remote":
                    for template_dir in self.env.loader.searchpath:
                        files = (
                            os.path.join(template_dir, "resource", "js", "combined.js"),
                            os.path.join(template_dir, "resource", "css", "combined-embedded.css"),
                            os.path.join(template_dir, "resource", "font", "apidoc.eot"),
                            os.path.join(template_dir, "resource", "font", "apidoc.woff"),
                            os.path.join(template_dir, "resource", "font", "apidoc.ttf"),
                            os.path.join(template_dir, "resource", "font", "source-code-pro.eot"),
                            os.path.join(template_dir, "resource", "font", "source-code-pro.woff"),
                            os.path.join(template_dir, "resource", "font", "source-code-pro.ttf"),
                        )

                        for file in files:
                            filename = os.path.basename(file)
                            dirname = os.path.basename(os.path.dirname(file))

                            if not os.path.exists(os.path.join(dir, dirname)):
                                os.makedirs(os.path.join(dir, dirname))
                            if os.path.exists(file):
                                shutil.copyfile(file, os.path.join(dir, dirname, filename))
                            else:
                                logging.getLogger().warn('Missing resource file "%s". If you run apidoc in virtualenv, run "%s"' % (filename, "python setup.py resources"))

            open(self.output, "w").write(output)
