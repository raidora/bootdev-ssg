import unittest

from src.leafnode import LeafNode
from src.parentnode import ParentNode


class TestTextNode(unittest.TestCase):
    def test_no_tag_raises(self):
        nodes = [
            ParentNode("", [LeafNode("b", "ats")]),
            ParentNode(" ", [LeafNode("b", "ats")]),
            ParentNode(None, [LeafNode("b", "ats")]),
        ]
        for node in nodes:
            with self.assertRaises(ValueError) as ex:
                node.to_html()
            self.assertEqual(str(ex.exception), "(tag) cannot be empty")

    def test_no_props_render(self):
        nodes = [
            ParentNode("a", [LeafNode("b", "ats")], {}),
            ParentNode("a", [LeafNode("b", "ats")], None),
        ]
        for node in nodes:
            node.to_html()

    def test_no_children_raises(self):
        with self.assertRaises(ValueError) as ex:
            ParentNode("div", []),
        self.assertEqual(str(ex.exception), "(children) must be a list with at least one element")

        with self.assertRaises(ValueError) as ex:
            ParentNode("div", None),
        self.assertEqual(str(ex.exception), "(children) must be a list with at least one element")

        with self.assertRaises(ValueError) as ex:
            ParentNode("div", 2),
        self.assertEqual(str(ex.exception), "children must be a list")

        with self.assertRaises(ValueError) as ex:
            ParentNode("div", {}),
        self.assertEqual(str(ex.exception), "children must be a list")

    def test_node_render(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_nested_parents_render(self):
        node = ParentNode(
            "html",
            [
                ParentNode("head", [
                    LeafNode("title", "H1 text"),
                ], {'lang': 'eng'}),
                ParentNode("body", [
                    ParentNode("div", [
                        LeafNode("h1", "The big title"),
                    ]),
                    ParentNode("ul", [
                        LeafNode("li", "The first li"),
                        LeafNode("li", "The second li"),
                        LeafNode("li", "The third li"),
                        LeafNode("li", "The fourth li"),
                    ])
                ]),
            ]
        )
        self.assertEqual(node.to_html(), '<html><head lang="eng"><title>H1 text</title></head><body><div><h1>The big title</h1></div><ul><li>The first li</li><li>The second li</li><li>The third li</li><li>The fourth li</li></ul></body></html>')
