import unittest

from src.block_conversions import markdown_to_blocks, block_to_block_type, block_type_heading, block_type_paragraph, \
    block_type_code, block_type_quote, block_type_unordered_list, block_type_ordered_list, markdown_to_html_node


class TestBlockConversions(unittest.TestCase):

    def test_markdown_to_block(self):
        md = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items"""

        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 3)

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("This is a paragraph."), block_type_paragraph)

    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), block_type_heading)
        self.assertEqual(block_to_block_type("## Heading 2"), block_type_heading)
        self.assertEqual(block_to_block_type("###### Heading 6"), block_type_heading)

    def test_code(self):
        self.assertEqual(block_to_block_type("```code block```"), block_type_code)
        self.assertEqual(block_to_block_type("```\ncode block\n```"), block_type_code)

    def test_quote(self):
        self.assertEqual(block_to_block_type("> Quote line 1\n> Quote line 2"), block_type_quote)

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("* List item 1\n* List item 2"), block_type_unordered_list)
        self.assertEqual(block_to_block_type("- List item 1\n- List item 2"), block_type_unordered_list)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. List item 1\n2. List item 2"), block_type_ordered_list)
        self.assertEqual(block_to_block_type("1. First item\n2. Second item\n3. Third item"), block_type_ordered_list)

    def test_mixed_ordered_list(self):
        self.assertEqual(block_to_block_type("1. Item 1\n2. Item 2\n3. Item 3"), block_type_ordered_list)

    def test_invalid_ordered_list(self):
        self.assertEqual(block_to_block_type("1. Item 1\n2. Item 2\n4. Item 4"), block_type_paragraph)

    def test_full_markdown(self):
        f = open("../../content/majesty/index.md", "r")
        content = f.read()
        blocks = markdown_to_html_node(content)
        pass

