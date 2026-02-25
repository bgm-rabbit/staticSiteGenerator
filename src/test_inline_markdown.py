import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode("This is **bold** and **more bold**", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.PLAIN),
                TextNode("more bold", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode("This is **bolded text** here", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("bolded text", TextType.BOLD),
                TextNode(" here", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com)"
        )
        self.assertListEqual(
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
                ("another", "https://i.imgur.com")
            ], 
            matches
        )

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev")
            ],
            matches
        )

    def test_extract_links_excludes_images(self):
        # Testing that link extractor doesn't pick up image syntax
        text = "This is a ![image](https://url.com/img.png) and a [link](https://url.com)"
        links = extract_markdown_links(text)
        self.assertListEqual([("link", "https://url.com")], links)

    def test_extract_images_excludes_links(self):
        # Testing that image extractor doesn't pick up link syntax
        text = "This is a ![image](https://url.com/img.png) and a [link](https://url.com)"
        images = extract_markdown_images(text)
        self.assertListEqual([("image", "https://url.com/img.png")], images)

if __name__ == "__main__":
    unittest.main()
