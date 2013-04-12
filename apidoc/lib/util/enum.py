

class EnumMeta(type):

    """Meta class for Enum
    """
    def __new__(mcls, name, bases, attrs):
        """Class initialization
        """
        cls = type.__new__(mcls, name, bases, attrs)
        cls._Enum__index = _index = {}
        for base in reversed(bases):
            if hasattr(base, '_Enum__index'):
                _index.update(base._Enum__index)
        # create all of the instances of the new class
        for attr in attrs.keys():
            value = attrs[attr]
            if isinstance(value, int):
                evalue = int.__new__(cls, value)
                evalue._Enum__name = attr
                _index[value] = evalue
                setattr(cls, attr, evalue)
        return cls

    def __contains__(cls, value):
        if isinstance(value, str):
            return hasattr(cls, value)
        elif isinstance(value, int):
            return value in cls._Enum__index
        else:
            return False


class Enum(int, metaclass=EnumMeta):

    """Class base for Enum
    """

    def __new__(cls, value):
        """Class initialization
        """
        if isinstance(value, str):
            return getattr(cls, value)
        elif isinstance(value, int):
            return cls.__index[value]

    def __str__(self):
        """Return a string representation of the enum
        """
        return self.__name

    def __repr__(self):
        """Return a complexe representation of the enum
        """
        return "%s.%s" % (type(self).__name__, self.__name)
