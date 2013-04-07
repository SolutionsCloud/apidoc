def merge_dict(a, b):
    """Merge the dict a with the dict b and return the result
    """
    c = a.copy()
    c.update(b)
    return c
