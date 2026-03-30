import datetime
from enum import Enum
import re
import datetime

from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_text_nodes
from textnode import ( text_node_to_html_node, TextNode, TextType)


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "olist"
    ULIST = "ulist"
    NAV = "navbar"
    POSTED_DATE = "posted"



def markdown_to_blocks(md):
    blocks = md.split( "\n\n")
    filtered_blocks = []

    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def markdown_to_html_node(md):
    blocks = markdown_to_blocks(md)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

   
    if lines and lines[0].strip().startswith("```"):
        return BlockType.CODE

    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
            return BlockType.QUOTE

    if block.startswith("- "):
        is_navbar = True
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
            if not re.search(r"\[.*\]\(.*\)", line):
                is_navbar = False
        return BlockType.NAV if is_navbar else BlockType.ULIST

    if block.startswith("- "):
        for line in lines:
            if not line.startswith('- '):
                return BlockType.PARAGRAPH
        return BlockType.ULIST

    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST

    if block.startswith("date: ") or block.startswith("posted: "):
        return BlockType.POSTED_DATE

    return BlockType.PARAGRAPH


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type ==  BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.NAV:
        return nav_to_html_node(block)
    if block_type == BlockType.POSTED_DATE:
        return posted_date_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_text_nodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break

    if level + 1 > len(block):
        raise ValueError(f"invalid heading level: {level} ")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    """Converte code block com suporte a Prism.js"""
    lines = block.split("\n")
    
    if not lines or not lines[0].strip().startswith("```"):
        raise ValueError("invalid code block")
    
    # Extrai a linguagem
    first_line = lines[0].strip()
    language = ""
    if first_line != "```":
        language = first_line[3:].strip()
    
    # Pega o conteúdo
    if len(lines) >= 2:
        if lines[-1].strip() == "```":
            code_lines = lines[1:-1]
        else:
            code_lines = lines[1:]
    else:
        code_lines = []
    
    code_content = "\n".join(code_lines)
    
    # Escapa caracteres HTML
    code_content = code_content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    
    # Cria o nó pre com atributos
    pre_attrs = {}
    if language:
        pre_attrs["data-language"] = language
    
    # Cria o nó code com a classe de linguagem
    if language:
        code_node = LeafNode("code", code_content, {"class": f"language-{language.lower()}"})
    else:
        code_node = LeafNode("code", code_content)
    
    return ParentNode("pre", [code_node], pre_attrs)

def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        parts = item.split(". ", 1)
        text = parts[1]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items: 
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []

    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def nav_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("div", children, {"class": "pure-menu-list"}))

    ul_node = ParentNode("ul", html_items)
    return ParentNode("nav", [ul_node], {"class": "home-menu pure-menu pure-menu-horizontal pure-menu-fixed"})


def posted_date_to_html_node(block):
    """Converte um bloco de data de publicação para HTML"""
    
    # Extrai a data do bloco
    date_str = ""
    
    # Remove o prefixo e limpa
    if block.startswith("date: "):
        date_str = block[6:].strip()
    elif block.startswith("posted: "):
        date_str = block[8:].strip()
    elif block.startswith("[posted:"):
        date_str = block[8:].strip().rstrip("]")
    
    # Tenta fazer o parsing da data
    try:
        # Tenta diferentes formatos
        for fmt in ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d de %B de %Y", "%B %d, %Y"]:
            try:
                date_obj = datetime.strptime(date_str, fmt)
                break
            except:
                continue
        else:
            # Se não conseguir parsear, usa a string original
            date_obj = None
    except:
        date_obj = None
    
    # Formata a data para exibição
    if date_obj:
        meses = {
            1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
            5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
            9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
        }
        formatted_date = f"{date_obj.day} de {meses[date_obj.month]}, {date_obj.year}"
        iso_date = date_obj.strftime("%Y-%m-%d")
    else:
        formatted_date = date_str
        iso_date = date_str
    
    # Cria o HTML para a data
    date_html = f'''
    <div class="posted-date-block">
        <time datetime="{iso_date}">
           <i> {formatted_date}</i>
        </time>
    </div>
    '''
    
    # Retorna um LeafNode com o HTML da data
    return LeafNode("div", date_html, {"class": "posted-date"})
