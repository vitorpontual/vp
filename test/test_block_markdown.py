import unittest

from src.block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType
)

class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items"

            ]
        )


    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
        """

        block = markdown_to_blocks(md)

        self.assertEqual(
            block,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items"
            ]
        )


    def test_block_to_block_types(self):
        block = "# Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- more list ulist\n- more and more list"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)
        block = "1. list 1\n2. list 2\n3. list 3"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)
        
