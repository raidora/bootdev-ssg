from src.htmlnode import HTMLNode
from src.leafnode import LeafNode
from src.textnode import TextNode


def text_node_to_html_node(node: TextNode) -> HTMLNode:
    ntype = node.text_type

    if ntype == TextNode.text_type_text:
        return LeafNode(None, node.text)

    if ntype == TextNode.text_type_bold:
        return LeafNode("b", node.text)

    if ntype == TextNode.text_type_italic:
        return LeafNode("i", node.text)

    if ntype == TextNode.text_type_code:
        return LeafNode("code", node.text)

    if ntype == TextNode.text_type_link:
        return LeafNode("a", node.text, {'href': node.url})

    if ntype == TextNode.text_type_image:
        return LeafNode("img", None, {'src': node.url, 'alt': node.text})

    raise ValueError(f"Text type {node.text_type} is not a valid text_type")
