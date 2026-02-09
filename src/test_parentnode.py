import unittest
from htmlnode import ParentNode, LeafNode


class TestParentNode(unittest.TestCase):
    def test_props(self):
        child_node = LeafNode("span", "child", {"id": "child_1"})
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(parent_node.props_to_html(), ' class="container"')
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container"><span id="child_1">child</span></div>',
        )

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
