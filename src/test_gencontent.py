import unittest
from gencontent import extract_title

class TestGenContent(unittest.TestCase):
    def test_extract_title(self):
        # Basic case
        self.assertEqual(extract_title("# Hello"), "Hello")
        # With extra whitespace
        self.assertEqual(extract_title("#  Space Check  "), "Space Check")

    def test_extract_title_multiline(self):
        # h1 not on the first line
        md = "Some introductory text\n\n# Actual Title\nMore text"
        self.assertEqual(extract_title(md), "Actual Title")

    def test_extract_title_multiple_h1(self):
        # Should return the FIRST h1 found
        md = "# First Title\n\n# Second Title"
        self.assertEqual(extract_title(md), "First Title")

    def test_extract_title_none(self):
        # No h1 header (only h2)
        md = "## This is just an h2"
        with self.assertRaises(Exception) as cm:
            extract_title(md)
        self.assertEqual(str(cm.exception), "No h1 header found in markdown")

    def test_extract_title_no_space(self):
        # #WithoutSpace is technically not a header in many markdown flavors
        md = "#NoSpaceHeader"
        with self.assertRaises(Exception):
            extract_title(md)

    def test_extract_title_empty(self):
        # Completely empty document
        with self.assertRaises(Exception):
            extract_title("")
