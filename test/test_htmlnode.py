import unittest
from src.htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello world!!",
            None,
            {"class": "greeting","href": "https://url.com.br"}
        )

        self.assertEqual(node.props_to_html(), ' class="greeting" href="https://url.com.br"')


    def test_value(self):
        node = HTMLNode("p", "ok")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "ok")

    def test_repr(self):
        node = HTMLNode(
        "p",
        "whats a strange world",
        None,
        {"class": "primary", "id": "#01"}
    )
        self.assertEqual(node.__repr__(),
                    "HTMLNode(p, whats a strange world, children: None, {'class': 'primary', 'id': '#01'})"
                    ) 
    def test_leaf_to_html(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_link(self):
        node = LeafNode("a", "mundo da putaria", {"href": "https://mundodaputaria.com.br"})
        self.assertEqual(node.to_html(), '<a href="https://mundodaputaria.com.br">mundo da putaria</a>')

    def test_leaf_image(self):
        node = LeafNode("img", "", {"src": "https://chupachups", "alt": "chupachups"})
        self.assertEqual(node.to_html(), 
                         '<img src="https://chupachups" alt="chupachups"></img>')

    def test_to_html_with_chidlren(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),
                         "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), 
                        '<div><span><b>grandchild</b></span></div>')

    def test_to_html_with_many_child(self):
        node = ParentNode("p", [
            LeafNode("b", "Bold Text"),
            LeafNode(None, "Normal Text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal Text")
        ])

        self.assertEqual(
            node.to_html(),
            "<p><b>Bold Text</b>Normal Text<i>italic text</i>Normal Text</p>")

