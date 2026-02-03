import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_none(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_dict(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(
            tag="a",
            value="Google",
            props={"href": "https://www.google.com", "target": "_blank"},
        )
        out = node.props_to_html()

        # Order of dict keys is usually stable, but don't rely on it.
        self.assertTrue(out.startswith(" "))
        self.assertIn('href="https://www.google.com"', out)
        self.assertIn('target="_blank"', out)
        self.assertEqual(out.count(" "), 2)  # leading space + 1 separator between attrs


if __name__ == "__main__":
    unittest.main()

