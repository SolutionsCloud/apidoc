from apidoc.object.source import RootDto


class Source():

    """Provide tool to managed sources
    """

    def validate(self, sources):
        """Validate the format of sources
        """
        if not isinstance(sources, RootDto):
            raise Exception("Source object expected")
