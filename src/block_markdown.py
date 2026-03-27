from enum import Enum

from src.htmlnode import ParentNode
from src.inline_markdown import text_to_text_nodes
from src.textnode import ( text_node_to_html_node, TextNode, TextType)


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "olist"
    ULIST = "ulist"



def markdown_to_blocks(md):
    blocks = md.split( "\n")
    filtered_blocks = []

    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks
