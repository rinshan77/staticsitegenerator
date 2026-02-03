import unittest
from markdown_to_html import markdown_to_html_node


class TestMarkdownToHTML(unittest.TestCase):
    def test_wraps_in_div(self):
        md = "Hello"
        node = markdown_to_html_node(md)
        self.assertEqual(node.tag, "div")

    def test_two_blocks_make_two_children(self):
        md = "First paragraph\n\nSecond paragraph"
        node = markdown_to_html_node(md)
        self.assertEqual(len(node.children), 2)

    def test_code_block_is_pre_code(self):
        md = "```\nhello\n```"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertTrue(html.startswith("<div><pre><code>"))
        self.assertTrue(html.endswith("</code></pre></div>"))


if __name__ == "__main__":
    unittest.main()
