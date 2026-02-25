from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        # We only split "text" type nodes; others (bold, link, etc.) pass through as-is
        if old_node.text_type != TextType.PLAIN:
            new_nodes.append(old_node)
            continue
        
        split_nodes = []
        sections = old_node.text.split(delimiter)
        
        # If the length is even, it means there is an unmatched delimiter
        if len(sections) % 2 == 0:
            raise ValueError(f"Invalid markdown: matching {delimiter} not found")
        
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            # Even indexes are outside the delimiters (standard text)
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.PLAIN))
            # Odd indexes are inside the delimiters (the specific text_type)
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        
        new_nodes.extend(split_nodes)
        
    return new_nodes

def extract_markdown_images(text):
    # Regex breakdown:
    # !\[      -> matches the literal '!['
    # (.*?)    -> non-greedy capture group for the alt text
    # \]       -> matches the literal ']'
    # \(       -> matches the literal '('
    # (.*?)    -> non-greedy capture group for the URL
    # \)       -> matches the literal ')'
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    # Same as above, but without the leading '!'
    # We use a negative lookbehind (?<!!) to ensure we don't accidentally
    # match an image as a link.
    pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN:
            new_nodes.append(old_node)
            continue
        
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
            
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.PLAIN))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            original_text = sections[1]
        
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.PLAIN))
            
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN:
            new_nodes.append(old_node)
            continue
        
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
            
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.PLAIN))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
            
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.PLAIN))
            
    return new_nodes