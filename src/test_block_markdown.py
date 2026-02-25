import unittest
from block_markdown import BlockType, markdown_to_blocks, block_to_block_type

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

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_types(self):
        # Heading tests
        self.assertEqual(block_to_block_type("# heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("####### not heading"), BlockType.PARAGRAPH)
        
        # Code test
        self.assertEqual(block_to_block_type("```\ncode\n```"), BlockType.CODE)
        
        # Quote test
        self.assertEqual(block_to_block_type("> quote\n> more quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> quote\nnot quote"), BlockType.PARAGRAPH)
        
        # Unordered List test
        self.assertEqual(block_to_block_type("- item 1\n- item 2"), BlockType.ULIST)
        self.assertEqual(block_to_block_type("- item 1\n* item 2"), BlockType.PARAGRAPH)
        
        # Ordered List test
        self.assertEqual(block_to_block_type("1. first\n2. second"), BlockType.OLIST)
        self.assertEqual(block_to_block_type("1. first\n3. third"), BlockType.PARAGRAPH)
        
        # Paragraph test
        self.assertEqual(block_to_block_type("Just a normal paragraph."), BlockType.PARAGRAPH)

    def test_block_to_block_type_edge_cases(self):
        # Heading: No space after # is NOT a heading
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)
        # Heading: More than 6 # is NOT a heading
        self.assertEqual(block_to_block_type("####### TooMany"), BlockType.PARAGRAPH)
        
        # Code: Must start AND end with 3 backticks
        self.assertEqual(block_to_block_type("```\nNo ending"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("Missing start\n```"), BlockType.PARAGRAPH)
        
        # Quote: One bad line makes the whole block a paragraph
        bad_quote = "> line 1\n> line 2\nline 3 missing bracket"
        self.assertEqual(block_to_block_type(bad_quote), BlockType.PARAGRAPH)
        
        # Unordered List: Space is required after the dash
        self.assertEqual(block_to_block_type("-NoSpace"), BlockType.PARAGRAPH)
        # Unordered List: Mixed delimiters (* vs -) should fail if your logic only checks -
        self.assertEqual(block_to_block_type("- Item 1\n* Item 2"), BlockType.PARAGRAPH)
        
        # Ordered List: Must start at 1
        self.assertEqual(block_to_block_type("2. starts at two"), BlockType.PARAGRAPH)
        # Ordered List: Must increment by exactly 1
        bad_olist = "1. first\n2. second\n4. skipped three"
        self.assertEqual(block_to_block_type(bad_olist), BlockType.PARAGRAPH)
        # Ordered List: Missing space after dot
        self.assertEqual(block_to_block_type("1.NoSpace"), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
