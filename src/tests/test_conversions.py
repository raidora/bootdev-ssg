import unittest

from src.conversions import text_node_to_html_node
from src.textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_text_node(self):
        node = text_node_to_html_node(TextNode("Hello", TextNode.text_type_text))
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, "Hello")

    def test_bold_node(self):
        node = text_node_to_html_node(TextNode("Hello", TextNode.text_type_bold))
        self.assertEqual(node.tag, "b")
        self.assertEqual(node.value, "Hello")

    def test_italic_node(self):
        node = text_node_to_html_node(TextNode("Hello", TextNode.text_type_italic))
        self.assertEqual(node.tag, "i")
        self.assertEqual(node.value, "Hello")

    def test_code_node(self):
        node = text_node_to_html_node(TextNode("Hello", TextNode.text_type_code))
        self.assertEqual(node.tag, "code")
        self.assertEqual(node.value, "Hello")

    def test_link_node(self):
        node = text_node_to_html_node(TextNode("Hello", TextNode.text_type_link, "https://test.test"))
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.props, {'href': "https://test.test"})

    def test_image_node(self):
        node = text_node_to_html_node(TextNode("Hello", TextNode.text_type_image, "https://test.test"))
        self.assertEqual(node.tag, "img")
        self.assertEqual(node.props, {'src': "https://test.test", 'alt': "Hello"})
