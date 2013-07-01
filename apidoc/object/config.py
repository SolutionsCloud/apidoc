class Config(dict):

    """Represente a config Object
    """

    def __init__(self):
        """Class instantiation
        """
        self["input"] = {
            "directories": None,
            "files": None,
            "arguments": None,
            "validate": True
        }

        self["filter"] = {
            "versions": {
                "includes": None,
                "excludes": None,
            },
            "categories": {
                "includes": None,
                "excludes": None,
            },
        }

        self["output"] = {
            "location": "stdout",
            "template": "default",
            "componants": "local",
            "layout": "default"
        }
