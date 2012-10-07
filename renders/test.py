# -*- coding: utf-8 -*-

import unittest
from ebook import Ebook


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.book = Ebook()

    def test_1_line(self):
        text = "one line of text"
        self.assertEqual(self.book.escape_text_to_html(text),
                        text)

    def test_2_line(self):
        text = "one line of text\nsecond line"
        self.assertEqual(self.book.escape_text_to_html(text),
                        text)

    def test_unicode(self):
        text = u"§"
        self.assertEqual(self.book.escape_text_to_html(text),
                        "&#167;")

    def test_greater_than_and_less_than(self):
        text = "0 < 1 and 2 > 1"
        self.assertEqual(self.book.escape_text_to_html(text),
                        "0 &lt; 1 and 2 &gt; 1")

    def test_html_tags(self):

        text = "<b>bold</b> plain text"
        self.assertEqual(self.book.escape_text_to_html(text), text)

    def test_more_html_tags(self):
        text = "<i>bold</i> plain text"
        self.assertEqual(self.book.escape_text_to_html(text),
                         text)

        text = "<b>bold</b> &#x300; plain text"
        self.assertEqual(self.book.escape_text_to_html(text),
                         text)

    def test_escaped_chars_are_ignored(self):

        text = r"\&amp;"
        self.assertEqual(self.book.escape_text_to_html(text),
                         "&amp;amp;")

        text = r"\<b\> <b> \<b\> \<b>"
        self.assertEqual(self.book.escape_text_to_html(text),
                         "&lt;b&gt; <b> &lt;b&gt; &lt;b&gt;")


if __name__ == '__main__':
    unittest.main()
