import unittest

from src.inline_markdown import split_nodes_delimiter, text_to_text_nodes, split_node_image, extract_markdown_image, split_node_link
from src.textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        nodes = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([nodes], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT)
            ], 
            new_nodes
        )


    def test_delim_bold_double(self):
        node = TextNode(
        "This is text **GOD** word and **GOOD**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text ", TextType.TEXT),
                TextNode("GOD", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("GOOD", TextType.BOLD)
            ],
            new_nodes
        )

    def test_delim_bold_multword(self):
        node = TextNode("This is **a text**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node],"**", TextType.BOLD)

        self.assertListEqual([
            TextNode("This is ", TextType.TEXT),
            TextNode("a text", TextType.BOLD)
        ], new_nodes)


    def test_delim_italic(self):
        node = TextNode("Text use _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual([
            TextNode("Text use ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC)
        ], new_nodes)

    def test_delim_bold_italic(self):
        node = TextNode("Text _italic_ and **bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD )

        self.assertListEqual([
            TextNode("Text ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold", TextType.BOLD)
        ], new_nodes)


    def test_delim_code(self):
        node = TextNode("Text `code` here!", TextType.TEXT)
        new_node = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertListEqual([
            TextNode("Text ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" here!", TextType.TEXT)
        ], new_node)


    def text_extract_markdown_images(self):
        matches = extract_markdown_image(
            "This is text with an ![image](url.png)"
        )
        self.assertListEqual([
            "image", "url.png"
        ], matches)


    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](url.png)", TextType.TEXT
        )
        new_nodes = split_node_image([node])
        self.assertListEqual([
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "url.png")
        ], new_nodes)


    def test_split_image_single(self):
        node = TextNode(
            "image2", TextType.IMAGE, "url.png"
        )
        new_nodes = split_node_image([node])

        self.assertListEqual([
            TextNode("image2", TextType.IMAGE, "url.png")
        ], new_nodes)


    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image1](url.com1) and ![image2](url.com2)", TextType.TEXT
        )
        new_nodes = split_node_image([node])

        self.assertListEqual([
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image1", TextType.IMAGE, "url.com1"),
            TextNode(" and ", TextType.TEXT),
            TextNode("image2", TextType.IMAGE, "url.com2")
        ], new_nodes)


    def test_split_images_empty(self):
        node = TextNode("Empty", TextType.TEXT)
        new_nodes = split_node_image([node])

        self.assertListEqual([
            TextNode("Empty", TextType.TEXT)
        ], new_nodes)

    def test_split_images_alt_empty(self):
        node = TextNode("Empty Alt ![](url)", TextType.TEXT)
        new_nodes = split_node_image([node])

        self.assertListEqual([
            TextNode("Empty Alt ", TextType.TEXT),
            TextNode("", TextType.IMAGE, "url")
        ], new_nodes)

    def test_split_image_text_final(self):
        node = TextNode("![image](url) text", TextType.TEXT)
        new_nodes = split_node_image([node])

        self.assertListEqual([
            TextNode("image", TextType.IMAGE, "url"),
            TextNode(" text", TextType.TEXT)
        ], new_nodes)



    def test_split_links(self):
        node = TextNode(
            "Two links here [link1](url1) and [link2](url2)", TextType.TEXT
        )
        new_nodes = split_node_link([node])

        self.assertListEqual([
            TextNode("Two links here ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "url1"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url2")
        ], new_nodes)


    def test_split_link_linked(self):
        node = TextNode(
            "[](url)", TextType.TEXT
        )
        new_nodes = split_node_link([node])

        self.assertListEqual([
            TextNode("", TextType.LINK, "url")
        ], new_nodes)


    def test_split_link_ultra(self):
        node = TextNode(
            "[test1](url1) --Texto-- [test2](url2) [](url3) last text", TextType.TEXT
        )
        new_nodes = split_node_link([node])

        self.assertListEqual([
            TextNode("test1", TextType.LINK, "url1"),
            TextNode(" --Texto-- ", TextType.TEXT),
            TextNode("test2", TextType.LINK, 'url2'),
            TextNode(" ", TextType.TEXT),
            TextNode("", TextType.LINK, "url3"),
            TextNode(" last text", TextType.TEXT)
        ], new_nodes)


    def test_text_to_textnodes(self): 
        nodes = text_to_text_nodes(
            "This is **text** with an _italic_ word and `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) [link](https://boot.dev)"
        )

        self.assertListEqual([
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT), 
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev")

        ], nodes)




if __name__ == "__main__":
    unittest.main()
