import unittest

from src.conversions import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, \
    extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, map_into_zones
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

    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextNode.text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", TextNode.text_type_code)

        expected = [
            TextNode("This is text with a ", TextNode.text_type_text),
            TextNode("code block", TextNode.text_type_code),
            TextNode(" word", TextNode.text_type_text),
        ]

        self.assertEqual(new_nodes, expected)

    def test_extract_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        self.assertEqual(extract_markdown_images(text), [
            ("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")])

    def test_extract_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        self.assertEqual(extract_markdown_links(text),
                         [("link", "https://www.example.com"), ("another", "https://www.example.com/another")])

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png) and some more",
            TextNode.text_type_text,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TextNode.text_type_text),
            TextNode("image", TextNode.text_type_image,
                     "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and another ", TextNode.text_type_text),
            TextNode(
                "second image", TextNode.text_type_image,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
            ),
            TextNode(" and some more", TextNode.text_type_text),
        ]
        self.assertEqual(expected, new_nodes)

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with an [linkyboi](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another [second linkyboi](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png) and some more",
            TextNode.text_type_text,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with an ", TextNode.text_type_text),
            TextNode("linkyboi", TextNode.text_type_link,
                     "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and another ", TextNode.text_type_text),
            TextNode(
                "second linkyboi", TextNode.text_type_link,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
            ),
            TextNode(" and some more", TextNode.text_type_text),
        ]
        self.assertEqual(expected, new_nodes)

    def test_text_to_nodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextNode.text_type_text),
            TextNode("text", TextNode.text_type_bold),
            TextNode(" with an ", TextNode.text_type_text),
            TextNode("italic", TextNode.text_type_italic),
            TextNode(" word and a ", TextNode.text_type_text),
            TextNode("code block", TextNode.text_type_code),
            TextNode(" and an ", TextNode.text_type_text),
            TextNode("image", TextNode.text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a ", TextNode.text_type_text),
            TextNode("link", TextNode.text_type_link, "https://boot.dev"),
        ]
        self.assertEqual(expected, new_nodes)

    def test_zone_mapper(self):
        text = "This *boob* is text with a *hallo* bit bit ibitus"
        res = map_into_zones(text, "*")
        expected = [('T', 0), ('h', 0), ('i', 0), ('s', 0), (' ', 0), ('*', 1), ('b', 1), ('o', 1), ('o', 1), ('b', 1), ('*', 1), (' ', 0), ('i', 0), ('s', 0), (' ', 0), ('t', 0), ('e', 0), ('x', 0), ('t', 0), (' ', 0), ('w', 0), ('i', 0), ('t', 0), ('h', 0), (' ', 0), ('a', 0), (' ', 0), ('*', 1), ('h', 1), ('a', 1), ('l', 1), ('l', 1), ('o', 1), ('*', 1), (' ', 0), ('b', 0), ('i', 0), ('t', 0), (' ', 0), ('b', 0), ('i', 0), ('t', 0), (' ', 0), ('i', 0), ('b', 0), ('i', 0), ('t', 0), ('u', 0), ('s', 0)]
        self.assertEqual(res, expected)

        text = "This **boob** is text with a *hallo* bit bit ibitus"
        res = map_into_zones(text, "**")
        expected = [('T', 0), ('h', 0), ('i', 0), ('s', 0), (' ', 0), ('*', 1), ('*', 1), ('b', 1), ('o', 1), ('o', 1), ('b', 1), ('*', 1), ('*', 1), (' ', 0), ('i', 0), ('s', 0), (' ', 0), ('t', 0), ('e', 0), ('x', 0), ('t', 0), (' ', 0), ('w', 0), ('i', 0), ('t', 0), ('h', 0), (' ', 0), ('a', 0), (' ', 0), ('*', 0), ('h', 0), ('a', 0), ('l', 0), ('l', 0), ('o', 0), ('*', 0), (' ', 0), ('b', 0), ('i', 0), ('t', 0), (' ', 0), ('b', 0), ('i', 0), ('t', 0), (' ', 0), ('i', 0), ('b', 0), ('i', 0), ('t', 0), ('u', 0), ('s', 0)]
        self.assertEqual(res, expected)
