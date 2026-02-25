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