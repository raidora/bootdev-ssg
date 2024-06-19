import re

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
        return LeafNode("img", "", {'src': node.url, 'alt': node.text})

    raise ValueError(f"Text type {node.text_type} is not a valid text_type")


text_zone = 0
delim_zone = 1


def block_content_to_html(block):
    text_nodes = text_to_textnodes(block)
    html = ""

    for node in text_nodes:
        html += text_node_to_html_node(node).to_html()

    return html


def map_into_zones(text, delimiter):
    text_classification = []
    delim_zone_buffer = 0
    in_delim_zone = False

    for idx, char in enumerate(text):
        chunk = text[idx:idx + len(delimiter)]

        if delim_zone_buffer > 0:
            delim_zone_buffer -= 1
            if delim_zone_buffer == 0:
                in_delim_zone = False

        if chunk == delimiter and in_delim_zone:
            delim_zone_buffer = len(delimiter)
        elif chunk == delimiter and not in_delim_zone:
            in_delim_zone = True

        if in_delim_zone or delim_zone_buffer > 0:
            text_classification.append((char, delim_zone))
        else:
            text_classification.append((char, text_zone))

    return text_classification


def split_nodes_delimiter(old_nodes: [TextNode], delimiter: str, text_type: str) -> [TextNode]:
    new_nodes = []
    buffer = ""

    for node in old_nodes:
        if node.text_type != TextNode.text_type_text:
            new_nodes.append(node)
            continue

        zones = map_into_zones(node.text, delimiter)

        for idx, zone_col in enumerate(zones):
            col_char = zone_col[0]
            col_type = zone_col[1]
            next_index = idx + 1
            buffer += col_char

            next_type = None
            try:
                next_type = zones[next_index][1]
            except IndexError:
                next_type = col_type + 1  # zone map ended. Make next check pass.

            if next_type != col_type:
                if col_type == delim_zone:
                    new_nodes.append(TextNode(buffer.strip(delimiter), text_type))
                else:
                    new_nodes.append(TextNode(buffer, TextNode.text_type_text))
                buffer = ""

    return new_nodes


def extract_markdown_images(text: str):
    return re.findall(r"!\[(.*?)]\((.*?)\)", text)


def extract_markdown_links(text: str):
    return re.findall(r"(?<!!)\[(.*?)]\((.*?)\)", text)


def split_nodes_image(old_nodes):
    cursor = 0
    counter = 0
    new_nodes = []

    for node in old_nodes:
        text = node.text
        imgs = extract_markdown_images(node.text)

        if len(imgs) == 0:
            new_nodes.append(node)

        for img in imgs:
            counter += 1
            splitting_string = f"![{img[0]}]({img[1]})"
            text_starting_at_cursor = text[cursor:]
            split_text = text_starting_at_cursor.split(splitting_string, 1)

            if len(split_text) > 1:
                new_nodes.append(TextNode(split_text[0], TextNode.text_type_text))
                cursor = len(split_text[0]) + len(splitting_string)
                new_nodes.append(TextNode(img[0], TextNode.text_type_image, img[1]))

                if counter == len(imgs) and len(split_text[1]) > 0:
                    new_nodes.append(TextNode(split_text[1], TextNode.text_type_text))

    return new_nodes


def split_nodes_link(old_nodes):
    cursor = 0
    counter = 0
    new_nodes = []

    for node in old_nodes:
        text = node.text
        links = extract_markdown_links(node.text)

        if len(links) == 0:
            new_nodes.append(node)

        for link in links:
            counter += 1
            splitting_string = f"[{link[0]}]({link[1]})"
            text_starting_at_cursor = text[cursor:]
            split_text = text_starting_at_cursor.split(splitting_string, 1)

            if len(split_text) > 1:
                new_nodes.append(TextNode(split_text[0], TextNode.text_type_text))
                cursor = len(split_text[0]) + len(splitting_string)
                new_nodes.append(TextNode(link[0], TextNode.text_type_link, link[1]))

                if counter == len(links) and len(split_text[1]) > 0:
                    new_nodes.append(TextNode(split_text[1], TextNode.text_type_text))

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextNode.text_type_text)]

    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)

    nodes = split_nodes_delimiter(nodes, "**", TextNode.text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", TextNode.text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", TextNode.text_type_code)

    return nodes


def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    blocks = [block.strip() for block in blocks]
    blocks = [block for block in blocks if block]

    return blocks
