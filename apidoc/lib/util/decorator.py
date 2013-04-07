

def add_property(attribute, type):
    """Add a property to a class
    """
    def decorator(cls):
        """Decorator
        """
        private = "_" + attribute

        def getAttr(self):
            """Property getter
            """
            if getattr(self, private) is None:
                setattr(self, private, type())
            return getattr(self, private)

        def setAttr(self, value):
            """Property setter
            """
            setattr(self, private, value)

        setattr(cls, attribute, property(getAttr, setAttr))
        setattr(cls, private, None)
        return cls

    return decorator
