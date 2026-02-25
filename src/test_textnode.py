import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        # Tests that two nodes with identical properties are equal
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        # Tests that two nodes with the same URL are equal
        node = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        # Tests that nodes with different text are NOT equal
        node = TextNode("This is text A", TextType.BOLD)
        node2 = TextNode("This is text B", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_type(self):
        # Tests that nodes with different text types are NOT equal
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        # Tests that nodes with different URLs are NOT equal
        node = TextNode("This is a text node", TextType.BOLD, "https://www.google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_url_none(self):
        # Explicitly testing equality when one URL is None and the other is a string
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_empty_text(self):
        # Tests that two nodes with empty strings are equal
        node = TextNode("", TextType.PLAIN)
        node2 = TextNode("", TextType.PLAIN)
        self.assertEqual(node, node2)

    def test_special_characters(self):
        # Tests handling of symbols, newlines, and unicode
        text = "Line 1\nLine 2! @#$%^&*()_+"
        node = TextNode(text, TextType.BOLD)
        node2 = TextNode(text, TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_is_none_by_default(self):
        # Verifies the default behavior of the url property
        node = TextNode("Check default", TextType.ITALIC)
        self.assertIsNone(node.url)

    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")

    def test_code(self):
        node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello')")

    def test_link(self):
        node = TextNode("Click me!", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me!")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_image(self):
        node = TextNode("Alt text", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props, 
            {"src": "https://www.boot.dev", "alt": "Alt text"}
        )

if __name__ == "__main__":
    unittest.main()
