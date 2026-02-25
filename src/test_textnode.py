import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()
