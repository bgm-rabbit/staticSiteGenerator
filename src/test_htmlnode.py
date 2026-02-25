import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_with_props(self):
        node = ParentNode(
            "div",
            [LeafNode("span", "hello")],
            {"class": "container", "id": "main"}
        )
        self.assertEqual(
            node.to_html(),
            '<div class="container" id="main"><span>hello</span></div>'
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold"),
                LeafNode(None, " and "),
                LeafNode("i", "italic"),
            ],
        )
        self.assertEqual(node.to_html(), "<h2><b>Bold</b> and <i>italic</i></h2>")


if __name__ == "__main__":
    unittest.main()
