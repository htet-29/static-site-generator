from extractor import extract_markdown_images, extract_markdown_links
from delimiter import split_nodes_images, text_to_textnodes, split_nodes_links
from textnode import TextNode, TextType


def main():
    node = TextNode(
        "This is text with an [first link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_links([node])
    print(new_nodes)


main()
