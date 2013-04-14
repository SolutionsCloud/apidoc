class Config(dict):

    """Represente a config Object
    """

    def __init__(self):
        """Class instantiation
        """
        self["input"] = {
            "directories": None,
            "files": None
        }

        self["filter"] = {
            "versions": {
                "includes": None,
                "excludes": None,
            },
            "sections": {
                "includes": None,
                "excludes": None,
            },
        }

        self["output"] = {
            "location": "stdout",
            "template": "default",
            "componants": "local"
        }
