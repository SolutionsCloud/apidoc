import json
from apidoc.lib.util.enum import Enum


def json_repr(obj):
    """Represent instance of a class as JSON.
    """

    def serialize(obj):
        """Recursively walk object's hierarchy.
        """
        if obj is None:
            return None
        if isinstance(obj, Enum):
            return str(obj)
        if isinstance(obj, (bool, int, float, str)):
            return obj
        if isinstance(obj, dict):
            obj = obj.copy()
            for key in sorted(obj.keys()):
                obj[key] = serialize(obj[key])
            return obj
        if isinstance(obj, list):
            return [serialize(item) for item in obj]
        if isinstance(obj, tuple):
            return tuple(serialize([item for item in obj]))
        if hasattr(obj, '__dict__'):
            return serialize(obj.__dict__)
        return repr(obj)

    return json.dumps(serialize(obj))
