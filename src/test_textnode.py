import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertEqual(node3.text_type, TextType.ITALIC)

    def test_text(self):
        text = "This is a text node"
        node = TextNode(text, TextType.BOLD)
        self.assertEqual(node.text, text)

    def test_texttype(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node.text_type, TextType.ITALIC)

    def test_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode(
            "This is a text nodel", TextType.BOLD, url="https://bootdev.com"
        )
        self.assertEqual(node.url, None)
        self.assertNotEqual(node2.url, None)


if __name__ == "__main__":
    unittest.main()
