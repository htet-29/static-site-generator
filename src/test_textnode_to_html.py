import unittest
from textnode import TextNode, TextType
from htmlnode import text_node_to_html_node


class TestTextNodeToHTML(unittest.TestCase):
    def test_text_type(self):
        textnode = TextNode("This is raw text", TextType.TEXT)
        htmlnode = text_node_to_html_node(textnode)
        self.assertEqual(htmlnode.to_html(), "This is raw text")

    def test_bold_type(self):
        textnode = TextNode("This is bold text", TextType.BOLD)
        htmlnode = text_node_to_html_node(textnode)
        self.assertEqual(htmlnode.to_html(), "<b>This is bold text</b>")

    def test_italic_type(self):
        textnode = TextNode("This is italic text", TextType.ITALIC)
        htmlnode = text_node_to_html_node(textnode)
        self.assertEqual(htmlnode.to_html(), "<i>This is italic text</i>")

    def test_code_type(self):
        textnode = TextNode("print('Hello world')", TextType.CODE)
        htmlnode = text_node_to_html_node(textnode)
        self.assertEqual(htmlnode.to_html(), "<code>print('Hello world')</code>")

    def test_link_type(self):
        textnode = TextNode("Click me!", TextType.LINK, "https://www.google.com")
        htmlnode = text_node_to_html_node(textnode)
        self.assertEqual(
            htmlnode.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def text_image_type(self):
        textnode = TextNode("This is image", TextType.IMAGE, "https://test_image.png")
        htmlnode = text_node_to_html_node(textnode)
        self.assertEqual(
            htmlnode.to_html(),
            '<img src="https://test_image.png" alt="this is image"></img>',
        )
