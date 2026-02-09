import unittest
from textnode import TextNode, TextType
from delimiter import split_nodes_delimiter, split_nodes_images, split_nodes_links


class TestDelimiter(unittest.TestCase):
    def test_bold(self):
        node = TextNode("This is one **bold text** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is one ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("bold text", TextType.BOLD))
        self.assertEqual(new_nodes[2], TextNode(" word", TextType.TEXT))

        two_bold_node = TextNode(
            "This is two **first bold** bold **second bold** text", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([two_bold_node], "**", TextType.BOLD)
        self.assertEqual(new_nodes[0], TextNode("This is two ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("first bold", TextType.BOLD))
        self.assertEqual(new_nodes[2], TextNode(" bold ", TextType.TEXT))
        self.assertEqual(new_nodes[3], TextNode("second bold", TextType.BOLD))
        self.assertEqual(new_nodes[4], TextNode(" text", TextType.TEXT))

    def test_italic(self):
        node = TextNode("This is one _italic text_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is one ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("italic text", TextType.ITALIC))
        self.assertEqual(new_nodes[2], TextNode(" word", TextType.TEXT))

        two_bold_node = TextNode(
            "This is two _first italic_ italic _second italic_ text", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([two_bold_node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes[0], TextNode("This is two ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("first italic", TextType.ITALIC))
        self.assertEqual(new_nodes[2], TextNode(" italic ", TextType.TEXT))
        self.assertEqual(new_nodes[3], TextNode("second italic", TextType.ITALIC))
        self.assertEqual(new_nodes[4], TextNode(" text", TextType.TEXT))

    def test_code(self):
        node = TextNode("This is one `code block` block", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is one ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("code block", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode(" block", TextType.TEXT))

        two_bold_node = TextNode(
            "This is two `first block` code `second block` block", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([two_bold_node], "`", TextType.CODE)
        self.assertEqual(new_nodes[0], TextNode("This is two ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("first block", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode(" code ", TextType.TEXT))
        self.assertEqual(new_nodes[3], TextNode("second block", TextType.CODE))
        self.assertEqual(new_nodes[4], TextNode(" block", TextType.TEXT))

    def test_all(self):
        bold_node = TextNode("This is block text", TextType.BOLD)
        italic_node = TextNode("This is italic text", TextType.ITALIC)
        code_node = TextNode("This is code block", TextType.CODE)
        new_nodes = split_nodes_delimiter(
            [bold_node, italic_node, code_node], "**", TextType.BOLD
        )
        self.assertEqual(len(new_nodes), 3)


class TestSplitImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

        node2 = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node2])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


class TestSplitLinks(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with an [first link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode(
                    "first link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"
                ),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

        node2 = TextNode(
            "[first link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node2])
        self.assertListEqual(
            [
                TextNode(
                    "first link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"
                ),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
