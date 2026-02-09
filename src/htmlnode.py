from textnode import TextType


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        return "".join([f' {key}="{value}"' for key, value in self.props.items()])

    def __repr__(self) -> str:
        props = self.props_to_html()
        if self.children is not None:
            return f"<{self.tag}{props}>{self.value} {self.children}</{self.tag}>"

        return f"<{self.tag}{props}>{self.value} {self.children}</{self.tag}>"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None) -> None:
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        props = self.props_to_html()
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        props = self.props_to_html()
        if self.tag is None and self.value is not None:
            return self.value
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None) -> None:
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag is missing")
        if self.children is None:
            raise ValueError("Children is missing")
        props = self.props_to_html()
        html = f"<{self.tag}{props}>"
        for child in self.children:
            html += child.to_html()
        html += f"</{self.tag}>"
        return html


def text_node_to_html_node(textnode):
    match textnode.text_type:
        case TextType.TEXT:
            return LeafNode(None, textnode.text)
        case TextType.BOLD:
            return LeafNode("b", textnode.text)
        case TextType.ITALIC:
            return LeafNode("i", textnode.text)
        case TextType.CODE:
            return LeafNode("code", textnode.text)
        case TextType.LINK:
            return LeafNode("a", textnode.text, {"href": textnode.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": textnode.url, "alt": textnode.text})
        case _:
            raise Exception("Unkown Text Type")
