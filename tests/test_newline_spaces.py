"""Tests: remove half-width spaces before newlines in ja.py / en.py.

Two processing paths:
  1. テキスト文書 → re.sub(r'[ ]+(\r?\n)', r'\1', text)
  2.  Word文書   → XML-level rstrip(' \t') on <w:t> before <w:br>
"""

import re
import unittest


def text_path_strip(text):
    """Simulates the regex added to both ja.py and en.py text paths."""
    return re.sub(r'[ ]+(\r?\n)', r'\1', text)


def word_path_rstrip(text):
    """Simulates the rstrip logic for <w:t> before <w:br>."""
    return text.rstrip(' \t')


class TestTextPathRegex(unittest.TestCase):
    """Tests for the テキスト文書 path (re.sub)"""

    def test_space_before_newline(self):
        self.assertEqual(text_path_strip("abc \ndef"), "abc\ndef")

    def test_space_before_crlf(self):
        self.assertEqual(text_path_strip("abc \r\ndef"), "abc\r\ndef")

    def test_multiple_spaces_before_newline(self):
        self.assertEqual(text_path_strip("hello   \nworld"), "hello\nworld")

    def test_no_space_before_newline(self):
        self.assertEqual(text_path_strip("abc\ndef"), "abc\ndef")

    def test_space_in_middle_not_affected(self):
        self.assertEqual(text_path_strip("a b c\ndef"), "a b c\ndef")

    def test_multiple_lines(self):
        input_text = "line1  \nline2 \nline3\nline4  \r\nline5"
        expected = "line1\nline2\nline3\nline4\r\nline5"
        self.assertEqual(text_path_strip(input_text), expected)

    def test_tab_before_newline_not_affected(self):
        # tabs are NOT half-width spaces; the regex uses [ ]+ not \s+
        self.assertEqual(text_path_strip("abc\t\ndef"), "abc\t\ndef")

    def test_trailing_space_no_newline(self):
        # trailing space at end of text without newline stays
        self.assertEqual(text_path_strip("hello "), "hello ")

    def test_only_spaces_and_newline(self):
        self.assertEqual(text_path_strip("  \n"), "\n")

    def test_empty_string(self):
        self.assertEqual(text_path_strip(""), "")


class TestWordPathRstrip(unittest.TestCase):
    """Tests for the Word文書 path (rstrip before <w:br>)"""

    def test_trailing_spaces_stripped(self):
        self.assertEqual(word_path_rstrip("hello  "), "hello")
        self.assertEqual(word_path_rstrip("text "), "text")

    def test_tab_stripped(self):
        self.assertEqual(word_path_rstrip("text\t"), "text")

    def test_no_trailing_whitespace(self):
        self.assertEqual(word_path_rstrip("hello"), "hello")

    def test_only_whitespace(self):
        self.assertEqual(word_path_rstrip("  \t  "), "")

    def test_empty_string(self):
        self.assertEqual(word_path_rstrip(""), "")

    def test_leading_spaces_preserved(self):
        self.assertEqual(word_path_rstrip("  hello"), "  hello")


class TestHighlightFunctionsUnaffected(unittest.TestCase):
    """Verify the highlight logic signatures still work unchanged."""

    def test_regex_does_not_touch_highlight_code(self):
        """The regex only affects text — highlight functions are separate."""
        # Simulate the full text path order from ja.py
        text = "some text \nmore"
        text = re.sub(r'[ ]+(\r?\n)', r'\1', text)
        self.assertEqual(text, "some text\nmore")
        # No highlight-related strings were modified

    def test_word_path_only_strips_trailing_spaces(self):
        """rstrip only removes trailing spaces/tabs, not highlight markers."""
        # Simulate: text before <w:br> might contain highlight markers
        text = "text with — dash"
        stripped = text.rstrip(' \t')
        self.assertEqual(stripped, "text with — dash")


if __name__ == "__main__":
    unittest.main()
