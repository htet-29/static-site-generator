import re
from textnode import TextType, TextNode
from extractor import extract_markdown_images, extract_markdown_links


def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    nodes = [node]
    nodes = split_nodes_links(nodes)
    nodes = split_nodes_images(nodes)
    if "**" in text:
        nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    if "`" in text:
        nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    if "_" in text:
        nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    return nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            nodes = []
            parts = split_nodes(node.text, delimiter, text_type)
            for part in parts:
                if not part:
                    continue
                if part.startswith(delimiter):
                    text = part.strip(delimiter)
                    bold_node = TextNode(text, text_type)
                    nodes.append(bold_node)
                else:
                    text_node = TextNode(part, TextType.TEXT)
                    nodes.append(text_node)
            new_nodes.extend(nodes)
        else:
            new_nodes.append(node)

    return new_nodes


def split_nodes(text, delimiter, text_type):
    match text_type:
        case TextType.BOLD:
            if delimiter != "**":
                raise Exception("Invalid delimiter for bold text (Use '**' instead)")
            return re.split(r"(\*\*[^*]+\*\*)", text)
        case TextType.ITALIC:
            if delimiter != "_":
                raise Exception("Invalid delimiter for italic text (Use '_' instead)")
            return re.split(r"(_[^_]+_)", text)
        case TextType.CODE:
            if delimiter != "`":
                raise Exception("Invalid delimiter for code block (Use '`' instead)")
            return re.split(r"(`[^`]+`)", text)
    return []


def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        attributes = extract_markdown_images(node.text)
        if len(attributes) == 0:
            new_nodes.append(node)
        text = node.text
        for attribute in attributes:
            before, after = text.split(f"![{attribute[0]}]({attribute[1]})")
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(attribute[0], TextType.IMAGE, attribute[1]))
            if not after:
                break
            if "![" in after:
                text = after
            else:
                new_nodes.append(TextNode(after, TextType.TEXT))
    return new_nodes


def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        attributes = extract_markdown_links(node.text)
        if len(attributes) == 0:
            new_nodes.append(node)
        text = node.text
        for attribute in attributes:
            before, after = text.split(f"[{attribute[0]}]({attribute[1]})")
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(attribute[0], TextType.LINK, attribute[1]))
            if not after:
                break
            if "[" in after:
                text = after
            else:
                new_nodes.append(TextNode(after, TextType.TEXT))
    return new_nodes
