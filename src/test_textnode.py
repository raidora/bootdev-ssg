import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_text(self):
        # Text gets set
        node = TextNode("This is a text node", "bold", "https://test.test")
        self.assertEqual("This is a text node", node.text)

        # Raise on invalid inputs
        with self.assertRaises(TypeError) as ex:
            TextNode(None, "bold", "https://test.test")
        self.assertEqual("Text must be of type string", str(ex.exception))

        with self.assertRaises(TypeError) as ex:
            TextNode(2, "bold")
        self.assertEqual("Text must be of type string", str(ex.exception))

        with self.assertRaises(TypeError) as ex:
            TextNode({2: "warm"}, "bold", "some url too")
        self.assertEqual("Text must be of type string", str(ex.exception))

        with self.assertRaises(TypeError) as ex:
            TextNode((2, "warm"), "bold")
        self.assertEqual("Text must be of type string", str(ex.exception))


    def test_text_type(self):
        # Text type gets set when valid
        node = TextNode("This is a text node", "bold", "https://test.test")
        self.assertEqual("bold", node.text_type)

        # Raise on invalid inputs
        with self.assertRaises(TypeError) as ex:
            TextNode("", "ham")
        self.assertEqual("text_type must be one of bold, italic, strikethrough, underline", str(ex.exception))

        with self.assertRaises(TypeError) as ex:
            TextNode("", {6: 6})
        self.assertEqual("text_type must be one of bold, italic, strikethrough, underline", str(ex.exception))

        with self.assertRaises(TypeError) as ex:
            TextNode("", None, "url was here --written by url ca 1992")
        self.assertEqual("text_type must be one of bold, italic, strikethrough, underline", str(ex.exception))

    def test_url(self):
        # Url gets set
        node = TextNode("This is a text node", "bold", "https://test.test")
        self.assertEqual("https://test.test", node.url)

        # Url should be nullable
        node = TextNode("This is a text node", "bold")
        self.assertEqual(None, node.url)

        node = TextNode("This is a text node", "bold", None)
        self.assertEqual(None, node.url)

        node = TextNode("This is a text node", "bold", "")
        self.assertEqual(None, node.url)

        # Raise error on bad type
        with self.assertRaises(TypeError) as ex:
            TextNode("", "bold", 2)
        self.assertEqual("url must be of type string", str(ex.exception))

        with self.assertRaises(TypeError) as ex:
            TextNode("", "bold", {2: "warm"})
        self.assertEqual("url must be of type string", str(ex.exception))

        with self.assertRaises(TypeError) as ex:
            TextNode("", "bold", (2, "warm"))
        self.assertEqual("url must be of type string", str(ex.exception))


if __name__ == "__main__":
    unittest.main()
