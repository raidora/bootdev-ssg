import unittest

from htmlnode import HTMLNode
from src.leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_node_render(self):
        node = LeafNode("p", "This is some text", {"href": "https://www.google.com", "data-testid": "testing"})
        self.assertEqual(node.to_html(), '<p href="https://www.google.com" data-testid="testing">This is some text</p>')

    def test_node_to_string(self):
        node = LeafNode("p", "This is some text", {"href": "https://www.google.com", "data-testid": "testing"})
        self.assertEqual(
            repr(node),
            "LeafNode(value=This is some text, tag=p, props={'href': 'https://www.google.com', 'data-testid': 'testing'})"
        )

    def test_empty_value_raises(self):
        nodes = [
            LeafNode("p", None, {"href": "https://www.google.com", "data-testid": "testing"}),
            LeafNode("p", "", {"href": "https://www.google.com", "data-testid": "testing"}),
            LeafNode("p", " ", {"href": "https://www.google.com", "data-testid": "testing"}),
        ]
        for node in nodes:
            with self.assertRaises(ValueError) as ex:
                node.to_html()
            self.assertEqual(str(ex.exception), "Value cannot be empty")

    def test_no_tag_returns_raw_text(self):
        nodes = [
            LeafNode(None, "This is some text", {"href": "https://www.google.com", "data-testid": "testing"}),
            LeafNode("", "This is some text", {"href": "https://www.google.com", "data-testid": "testing"}),
            LeafNode(" ", "This is some text", {"href": "https://www.google.com", "data-testid": "testing"}),
        ]
        for node in nodes:
            self.assertEqual(node.to_html(), "This is some text")
