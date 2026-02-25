import unittest
from block_markdown import markdown_to_blocks

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        # Original test case: Standard document
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        # Tests multiple newlines and trailing spaces between blocks
        md = """
# This is a heading  


This is a paragraph.


- Item 1
- Item 2

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph.",
                "- Item 1\n- Item 2",
            ],
        )

    def test_markdown_to_blocks_single(self):
        # Tests a document with only a single block
        md = "Just a single paragraph of text."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just a single paragraph of text."])

    def test_markdown_to_blocks_empty(self):
        # Tests empty input or input with only whitespace
        self.assertEqual(markdown_to_blocks(""), [])
        self.assertEqual(markdown_to_blocks("   \n\n  \n "), [])

    def test_markdown_to_blocks_indented(self):
        # Tests that leading/trailing whitespace is stripped correctly
        md = "   This paragraph has leading spaces.\n\n\tThis one starts with a tab."
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks, 
            ["This paragraph has leading spaces.", "This one starts with a tab."]
        )

if __name__ == "__main__":
    unittest.main()
