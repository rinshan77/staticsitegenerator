from blocktype import BlockType, block_to_block_type
from markdown_to_blocks import markdown_to_blocks
from htmlnode import ParentNode
from htmlnode import LeafNode

from text_to_textnodes import text_to_textnodes
from textnode import TextNode,TextType
from text_to_html import text_node_to_html_node 


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        btype = block_to_block_type(block)
        node = block_to_html_node(block, btype)
        children.append(node)

    return ParentNode("div", children)


# ---------- helpers ----------

def block_to_html_node(block, btype):
    if btype == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)

    if btype == BlockType.HEADING:
        return heading_to_html_node(block)

    if btype == BlockType.CODE:
        return code_to_html_node(block)

    if btype == BlockType.QUOTE:
        return quote_to_html_node(block)

    if btype == BlockType.UNORDERED_LIST:
        return ul_to_html_node(block)

    if btype == BlockType.ORDERED_LIST:
        return ol_to_html_node(block)

    raise ValueError(f"Unknown block type: {btype}")


def text_to_children(text):
    # inline parsing pipeline already solved by your earlier functions
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(n) for n in text_nodes]


def paragraph_to_html_node(block):
    # Replace internal newlines with spaces
    text = " ".join(block.split("\n"))
    return ParentNode("p", text_to_children(text))


def heading_to_html_node(block):
    # block format: ### Heading text
    i = 0
    while i < len(block) and block[i] == "#":
        i += 1
    level = i  # 1..6 guaranteed by your block type checker
    text = block[level + 1 :]  # skip "#...# " (space after hashes)
    return ParentNode(f"h{level}", text_to_children(text))


def code_to_html_node(block):
    # block format:
    # ```\n
    # code...\n
    # ```
    # Remove the starting "```" line and ending "```"
    lines = block.split("\n")
    # drop first line (```), drop last line (```)
    code_text = "\n".join(lines[1:-1])

    # IMPORTANT: no inline parsing inside code blocks
    code_leaf = LeafNode("code", code_text)
    return ParentNode("pre", [code_leaf])


def quote_to_html_node(block):
    # each line begins with ">" or "> "
    lines = block.split("\n")
    cleaned = []
    for line in lines:
        # remove leading ">" and optional single space
        if line.startswith("> "):
            cleaned.append(line[2:])
        elif line.startswith(">"):
            cleaned.append(line[1:])
        else:
            cleaned.append(line)

    text = " ".join(cleaned)
    return ParentNode("blockquote", text_to_children(text))


def ul_to_html_node(block):
    # lines: "- item"
    items = []
    for line in block.split("\n"):
        item_text = line[2:]  # remove "- "
        items.append(ParentNode("li", text_to_children(item_text)))
    return ParentNode("ul", items)


def ol_to_html_node(block):
    # lines: "1. item", "2. item", ...
    items = []
    for line in block.split("\n"):
        # split only once: "1. " then rest
        parts = line.split(". ", 1)
        item_text = parts[1] if len(parts) == 2 else ""
        items.append(ParentNode("li", text_to_children(item_text)))
    return ParentNode("ol", items)

