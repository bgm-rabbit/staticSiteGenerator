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
