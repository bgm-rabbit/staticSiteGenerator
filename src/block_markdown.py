from enum import Enum

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
