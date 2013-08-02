

def to_boolean(val):
    """Cast an object to a boolean value
    """
    return str(val).lower() in ("true", "1", "yes", "y")
