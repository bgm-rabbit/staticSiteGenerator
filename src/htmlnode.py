class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        # A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        self.tag = tag
        # A string representing the value of the HTML tag (e.g. the text inside a paragraph)
        self.value = value
        # A list of HTMLNode objects representing the children of this node
        self.children = children
        # A dictionary of key-value pairs representing the attributes of the HTML tag.
        # For example, a link (<a> tag) might have {"href": "https://www.google.com"}
        self.props = props
        
    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if not self.props:
            return ""
        
        props_html = ""
        for key, value in self.props.items():
            props_html += f' {key}="{value}"'
        return props_html
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if not self.value:
            raise ValueError("All leaf nodes must have a value")
        
        # If there is no tag, return the value as raw text
        if not self.tag:
            return self.value
        
        # Otherwise, render as an HTML tag with properties and the value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("All parent nodes must have a tag")
        
        if not self.children:
            raise ValueError("All parent nodes must have children")
        
        # Recursive step: call to_html() on every child and join the results
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
            
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"