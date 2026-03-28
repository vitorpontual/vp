import unittest
from src.textnode import TextType,TextNode, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = ("This is war", TextType.TEXT)
        node2 = ("This is war", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = ("This is word", TextType.TEXT)
        node2 =("This is word", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is text Node", TextType.TEXT)
        node2 = TextNode("This is a text node2", TextType.TEXT)
        self.assertNotEqual(node, node2)



class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


    def test_image(self):
        node = TextNode("This is image", TextType.IMAGE, "url")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "url", "alt": "This is image"}
        )
                         


if __name__ == "__main__":
    unittest.main()
