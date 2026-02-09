import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_None(self):
        htmlnode = HTMLNode()
        self.assertEqual(htmlnode.tag, None)
        self.assertEqual(htmlnode.value, None)
        self.assertEqual(htmlnode.children, None)
        self.assertEqual(htmlnode.props, None)

    def test_htmltag(self):
        htmlnode = HTMLNode("a")
        self.assertEqual(htmlnode.tag, "a")

    def test_value(self):
        htmlnode = HTMLNode(value="This is anchor tag")
        self.assertEqual(htmlnode.value, "This is anchor tag")

    def test_props_to_html(self):
        htmlnode = HTMLNode(
            props={"href": "https://www.google.com", "target": "_blank"}
        )
        props = htmlnode.props_to_html()
        self.assertEqual(props, ' href="https://www.google.com" target="_blank"')

    def test_repr(self):
        string = '<a href="https://www.google.com" target="_blank">This is anchor tag None</a>'
        html_node = HTMLNode(
            "a",
            "This is anchor tag",
            None,
            {"href": "https://www.google.com", "target": "_blank"},
        )
        self.assertEqual(str(html_node), string)
