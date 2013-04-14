import os
import shutil


class Template():

    """Provide tool to managed templates
    """

    def __init__(self):
        """Class instantiation
        """
        self.input = "default.html"
        self.output = "stdout"
        self.env = None

    def render(self, sources, config):
        """Render the documentation as defined in config Object
        """
        template = self.env.get_template(self.input)
        output = template.render(sources=sources, config=config["output"])
        if self.output == "stdout":
            os.system('clear')
            print(output)
        else:
            dir = os.path.dirname(self.output)
            if not os.path.exists(dir):
                os.makedirs(dir)
            if config["output"]["template"] == "default":
                if config["output"]["componants"] == "local":
                    for template_dir in self.env.loader.searchpath:
                        files = (
                            os.path.join(template_dir, "resource", "js", "apidoc.js"),
                            os.path.join(template_dir, "resource", "js", "jquery.min.js"),
                            os.path.join(template_dir, "resource", "js", "mousetrap.min.js"),
                            os.path.join(template_dir, "resource", "js", "bootstrap.min.js"),
                            os.path.join(template_dir, "resource", "css", "apidoc.css"),
                            os.path.join(template_dir, "resource", "css", "bootstrap.min.css"),
                            os.path.join(template_dir, "resource", "css", "bootstrap-responsive.min.css"),
                            os.path.join(template_dir, "resource", "img", "glyphicons-halflings.png"),
                            os.path.join(template_dir, "resource", "img", "glyphicons-halflings-white.png")
                        )

                        for file in files:
                            filename = os.path.basename(file)
                            dirname = os.path.basename(os.path.dirname(file))

                            if not os.path.exists(os.path.join(dir, dirname)):
                                os.makedirs(os.path.join(dir, dirname))
                            if os.path.exists(file) and not os.path.exists(os.path.join(dir, dirname, filename)):
                                shutil.copyfile(file, os.path.join(dir, dirname, filename))

                if config["output"]["componants"] == "remote":
                    for template_dir in self.env.loader.searchpath:
                        files = (
                            os.path.join(template_dir, "resource", "js", "apidoc.js"),
                            os.path.join(template_dir, "resource", "css", "apidoc.css"),
                        )

                        for file in files:
                            filename = os.path.basename(file)
                            dirname = os.path.basename(os.path.dirname(file))

                            if not os.path.exists(os.path.join(dir, dirname)):
                                os.makedirs(os.path.join(dir, dirname))
                            if os.path.exists(file) and not os.path.exists(os.path.join(dir, dirname, filename)):
                                shutil.copyfile(file, os.path.join(dir, dirname, filename))
            open(self.output, "w").write(output)
