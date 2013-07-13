import unittest

from apidoc.factory.source.element import Element as ElementFactory

from apidoc.object.source_raw import Element, Sampleable, Displayable


class TestElement(unittest.TestCase):

    def setUp(self):
        self.factory = ElementFactory()

    def test_set_common_datas__default(self):
        datas = {"description": "c", "sample": "foo"}
        element = Element()
        self.factory.set_common_datas(element, "o_name", datas)

        self.assertEqual("o_name", element.name)
        self.assertEqual("c", element.description)
        self.assertNotIn("display", vars(element))
        self.assertNotIn("sample", vars(element))
        self.assertNotIn("o_name", vars(element))

    def test_set_common_datas__sampleable(self):
        datas = {"description": "c", "sample": {"foo": "bar"}}
        element = Sampleable()
        self.factory.set_common_datas(element, "o_name", datas)

        self.assertEqual("{'foo': 'bar'}", element.sample)

    def test_set_common_datas__displayable(self):
        datas = {"description": "c", "display": "false", "label": "d"}
        element = Displayable()
        self.factory.set_common_datas(element, "o_name", datas)

        self.assertEqual(False, element.display)
        self.assertEqual("d", element.label)

    def test_set_common_datas__displayable_default(self):
        datas = {"description": "c"}
        element = Displayable()
        self.factory.set_common_datas(element, "o_name", datas)

        self.assertEqual(True, element.display)
