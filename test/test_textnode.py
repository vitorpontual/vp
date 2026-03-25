import unittest
from src.textnode import TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = ("This is war", TextType.TEXT)
        node2 = ("This is war", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = ("This is word", TextType.TEXT)
        node2 =("This is word", TextType.BOLD)
        self.assertNotEqual(node, node2)
