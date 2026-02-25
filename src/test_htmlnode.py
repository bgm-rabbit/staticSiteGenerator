import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_single(self):
        # Test a single attribute
        node = HTMLNode(props={"href": "https://www.google.com"})
        expected = ' href="https://www.google.com"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_multiple(self):
        # Test multiple attributes for spacing and quotes
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(props=props)
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_none(self):
        # Test that None or empty props return an empty string
        node = HTMLNode()
        node2 = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")
        self.assertEqual(node2.props_to_html(), "")

    def test_repr(self):
        # Test the string representation for debugging clarity
        node = HTMLNode("p", "Hello, world!", None, {"class": "primary"})
        expected = "HTMLNode(p, Hello, world!, children: None, {'class': 'primary'})"
        self.assertEqual(repr(node), expected)

    def test_leaf_to_html_p(self):
        # Basic paragraph test
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        # Link with attributes
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_raw_text(self):
        # Testing a node with no tag (should return raw text)
        node = LeafNode(None, "Just raw text.")
        self.assertEqual(node.to_html(), "Just raw text.")

    def test_leaf_to_html_bold(self):
        # Testing a different tag type
        node = LeafNode("b", "Bold move!")
        self.assertEqual(node.to_html(), "<b>Bold move!</b>")

    def test_leaf_to_html_no_value(self):
        # Testing that a ValueError is raised when value is missing
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
