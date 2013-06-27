from functools import total_ordering


@total_ordering
class Comparable():

    """Element who can be sorted
    """

    def get_comparable_values(self):
        """Return a tupple of values representing the unicity of the object
        """
        return ()

    def get_comparable_values_for_equality(self):
        """Return a tupple of values representing the unicity of the object
        """
        return self.get_comparable_values()

    def get_comparable_values_for_ordering(self):
        """Return a tupple of values representing the unicity of the object
        """
        return self.get_comparable_values()

    def __lt__(self, other):
        """Return true if self is lower than other
        """
        return self.get_comparable_values_for_ordering() < other.get_comparable_values_for_ordering()

    def __gt__(self, other):
        """Return true if self is lower than other
        """
        return self.get_comparable_values_for_ordering() > other.get_comparable_values_for_ordering()

    def __eq__(self, other):
        """Return true if self is equals to other
        """
        return type(self) is type(other) and self.get_comparable_values_for_equality() == other.get_comparable_values_for_equality()
