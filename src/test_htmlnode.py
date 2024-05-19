import unittest

from htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):

    def test_value_or_children_not_both(self):
        node = HTMLNode("h1", "imanode")
        self.assertEqual("h1", node.tag)

        node = HTMLNode(None, None, [node])
        self.assertEqual(None, node.tag)
        self.assertEqual(list, type(node.children))

        with self.assertRaises(ValueError) as ex:
            HTMLNode("h1", "imanode", [HTMLNode("b")])
        self.assertEqual("Tag should contain either value or children, not both", str(ex.exception))

    def test_props_happy(self):
        node = HTMLNode(props={"href": "https://test.test", "target": "_blank"})
        self.assertEqual('href="https://test.test" target="_blank"', node.props_to_html())
        self.assertEqual("_blank", node.props["target"])

