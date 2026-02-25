from enum import Enum
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node
from htmlnode import ParentNode, LeafNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def block_to_block_type(block):
    # Heading: 1-6 # followed by a space
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    # Code: starts and ends with ```
    if len(block) >= 6 and block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    lines = block.split("\n")
    
    # Quote: Every line starts with >
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    
    # Unordered List: Every line starts with "- "
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    
    # Ordered List: Every line starts with "i. " where i starts at 1 and increments
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    
    # Default
    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    # Split the document by double newlines
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    
    for block in blocks:
        # Strip leading/trailing whitespace from the block
        block = block.strip()
        # Only add the block if it's not an empty string
        if block != "":
            filtered_blocks.append(block)
            
    return filtered_blocks

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.QUOTE:
        return create_quote_node(block)
    if block_type == BlockType.ULIST:
        return create_ulist_node(block)
    if block_type == BlockType.OLIST:
        return create_olist_node(block)
    if block_type == BlockType.CODE:
        return create_code_node(block)
    if block_type == BlockType.HEADING:
        return create_heading_node(block)
    if block_type == BlockType.PARAGRAPH:
        return create_paragraph_node(block)
    raise ValueError("Invalid block type")

# --- Specific Block Handlers ---

def create_paragraph_node(block):
    # Join lines by space to ensure multi-line paragraphs render correctly
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def create_heading_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    # Slice off the '#' characters and the leading space
    content = block[level + 1 :]
    children = text_to_children(content)
    return ParentNode(f"h{level}", children)

def create_code_node(block):
    content = block[3:-3].strip("\n")
    # Using LeafNode directly prevents inline parsing!
    code_node = ParentNode("code", [LeafNode(None, content)])
    return ParentNode("pre", [code_node])


def create_quote_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def create_ulist_node(block):
    lines = block.split("\n")
    items = []
    for line in lines:
        # Remove the "- " prefix
        content = line[2:]
        children = text_to_children(content)
        items.append(ParentNode("li", children))
    return ParentNode("ul", items)

def create_olist_node(block):
    lines = block.split("\n")
    items = []
    for line in lines:
        # Remove the "1. " prefix (find the first space)
        content = line[line.find(" ") + 1 :]
        children = text_to_children(content)
        items.append(ParentNode("li", children))
    return ParentNode("ol", items)
