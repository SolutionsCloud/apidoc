from apidoc.object.source import Root


class Source():

    """Provide tool to managed sources
    """

    def validate(self, sources):
        """Validate the format of sources
        """
        if not isinstance(sources, Root):
            raise Exception("Source object expected")
