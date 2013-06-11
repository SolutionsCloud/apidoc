import unittest

from apidoc.object import Comparable


class TestSource(unittest.TestCase):

    def test_comparable_default(self):
        comparable = Comparable()

        self.assertEqual((), comparable.get_comparable_values())
        self.assertEqual((), comparable.get_comparable_values_for_equality())
        self.assertEqual((), comparable.get_comparable_values_for_ordering())

    def test_comparable___operators(self):
        class C1(Comparable):
            def __init__(self, name):
                self.name = name

            def get_comparable_values(self):
                return (self.name)

        comparable1 = C1("a")
        comparable2 = C1("b")

        self.assertTrue(comparable1 != comparable2)
        self.assertTrue(comparable1 < comparable2)
        self.assertTrue(comparable2 > comparable1)
        self.assertFalse(comparable1 == comparable2)

    def test_comparable_equality__with_one_property(self):
        class C1(Comparable):
            def __init__(self, name):
                self.name = name

            def get_comparable_values_for_equality(self):
                return (self.name)

        comparable1 = C1("a")
        comparable2 = C1("a")
        comparable3 = C1("b")

        self.assertEqual(comparable1, comparable2)
        self.assertNotEqual(comparable1, comparable3)

    def test_comparable_equality__with_multiple_property(self):
        class C1(Comparable):
            def __init__(self, name, description):
                self.name = name
                self.description = description

            def get_comparable_values_for_equality(self):
                return (self.name, self.description)

        comparable1 = C1("a", "b")
        comparable2 = C1("a", "b")
        comparable3 = C1("a", "c")

        self.assertEqual(comparable1, comparable2)
        self.assertNotEqual(comparable1, comparable3)

    def test_comparable_ordering__with_one_property(self):
        class C1(Comparable):
            def __init__(self, name):
                self.name = name

            def get_comparable_values_for_ordering(self):
                return (self.name)

        comparable1 = C1("a")
        comparable2 = C1("c")
        comparable3 = C1("b")

        self.assertEqual([comparable1, comparable3, comparable2], sorted([comparable1, comparable2, comparable3]))

    def test_comparable_ordering__with_multiple_property(self):
        class C1(Comparable):
            def __init__(self, name, description):
                self.name = name
                self.description = description

            def get_comparable_values_for_ordering(self):
                return (self.name, self.description)

        comparable1 = C1("a", "b")
        comparable2 = C1("b", "a")
        comparable3 = C1("a", "c")

        self.assertEqual([comparable1, comparable3, comparable2], sorted([comparable1, comparable2, comparable3]))
