import unittest

from generate_page import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_simple(self):
        md = "# Hello"
        self.assertEqual(extract_title(md), "Hello")

    def test_extract_title_strips_whitespace(self):
        md = "   #   Hello World   \n\nSome text"
        self.assertEqual(extract_title(md), "Hello World")

    def test_extract_title_ignores_h2(self):
        md = "## Not this\n\n# This one\n"
        self.assertEqual(extract_title(md), "This one")

    def test_extract_title_raises_if_missing(self):
        md = "## No h1 here\nJust text"
        with self.assertRaises(Exception):
            extract_title(md)


if __name__ == "__main__":
    unittest.main()

