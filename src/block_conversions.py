import re

from src.inline_conversions import text_node_to_html_node, text_to_textnodes, block_content_to_html
from src.leafnode import LeafNode
from src.parentnode import ParentNode

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    blocks = [block.strip() for block in blocks]
    blocks = [block for block in blocks if block]

    return blocks


def block_to_block_type(block):
    if block.startswith('#'):
        parts = block.split(' ', 1)
        if len(parts) > 1 and parts[0].count('#') in range(1, 7):
            return block_type_heading

    if block.startswith('```') and block.endswith('```'):
        return block_type_code

    if all(line.startswith('>') for line in block.split('\n')):
        return block_type_quote

    if all(line.startswith(('* ', '- ')) for line in block.split('\n')):
        return block_type_unordered_list

    lines = block.split('\n')
    if all(line.split('. ')[0].isdigit() for line in lines):
        numbers = [int(line.split('. ')[0]) for line in lines]
        if numbers == list(range(1, len(numbers) + 1)):
            return block_type_ordered_list

    return block_type_paragraph


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == block_type_quote:
            nodes.append(blockquote_to_htmlnode(block))
        elif block_type == block_type_unordered_list:
            nodes.append(unordered_list_to_htmlnode(block))
        elif block_type == block_type_ordered_list:
            nodes.append(ordered_list_to_htmlnode(block))
        elif block_type == block_type_code:
            nodes.append(code_to_htmlnode(block))
        elif block_type == block_type_code:
            nodes.append(code_to_htmlnode(block))
        elif block_type == block_type_heading:
            nodes.append(heading_to_htmlnode(block))
        elif block_type == block_type_paragraph:
            nodes.append(paragraph_to_htmlnode(block))

    return ParentNode("div", nodes)


def blockquote_to_htmlnode(block):
    block = re.sub(r"> ", "", block).strip()
    block = block_content_to_html(block)

    return LeafNode("blockquote", block)


def unordered_list_to_htmlnode(block):
    children = []

    li_items = block.split("\n")

    for li in li_items:
        clean_li = li.lstrip("- ")
        clean_li = block_content_to_html(clean_li)
        children.append(LeafNode("li", clean_li))

    return ParentNode("ul", children)


def ordered_list_to_htmlnode(block):
    children = []

    li_items = block.split("\n")

    for li in li_items:
        clean_li = re.sub(r'^\d\.', '', li).strip()
        clean_li = block_content_to_html(clean_li)
        children.append(LeafNode("li", clean_li))

    return ParentNode("ol", children)


def code_to_htmlnode(block):
    clean_block = block.strip("`")
    clean_block = block_content_to_html(clean_block)
    code_leaf = LeafNode("code", clean_block)
    return ParentNode("pre", [code_leaf])


def heading_to_htmlnode(block):
    hashtags = re.match(r"#+", block)
    g = hashtags.group(0)
    block = block_content_to_html(block.strip("#").strip())

    return LeafNode(f"h{len(g)}", block)


def paragraph_to_htmlnode(block):
    return LeafNode("p", block_content_to_html(block))
