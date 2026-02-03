from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    lines = block.split("\n")

    # heading: 1-6 #'s, then space
    if lines and lines[0].startswith("#"):
        i = 0
        while i < len(lines[0]) and lines[0][i] == "#":
            i += 1
        if 1 <= i <= 6 and len(lines[0]) > i and lines[0][i] == " ":
            return BlockType.HEADING

    # code block: starts with ```\n and ends with ```
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    # quote: every line starts with >
    if lines and all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # unordered list: every line starts with "- "
    if lines and all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # ordered list: "1. " then "2. " etc
    if lines:
        expected = 1
        ok = True
        for line in lines:
            prefix = f"{expected}. "
            if not line.startswith(prefix):
                ok = False
                break
            expected += 1
        if ok:
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

