#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import join, split
import time
import re

# tags that will be left as is when convert text/html to full html
HTML_TAGS = ('p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong', 'em', 'abbr',
             'acronym', 'address', 'bdo', 'blockquote', 'cite', 'q', 'code',
             'ins', 'del', 'dfn', 'kbd', 'pre', 'samp', 'var', 'br', 'br/',
             'br /', 'b', 'i', 'tt', 'sub', 'sup', 'big', 'small', 'hr')

SPACES = {'  ': '&#32;'}  # need a regex here ...

ESCAPES = {'€': '&euro;',
           '"': '&quot;',
           r'\&': '&amp;',
           '<': '&lt;',
           '>': '&gt;',
           #'...': '&hellip;'
           }


class Ebook(object):

    __slots__ = ['isbn', 'cover_art', 'title', 'primary_author',
                 'secondary_authors', 'language', 'publisher',
                 'date', 'renderer', 'chapters', 'template_folder',
                 'output_folder']

    def __init__(self):

        self.isbn = '0123456789'
        self.primary_author = "Anonymous"
        self.secondary_authors = []
        self.template_folder = join(split(__file__)[0], 'templates')
        self.language = 'en'
        self.publisher = "None"
        self.renderer = 'text'
        self.date = time.asctime()
        self.output_folder = "./"

    def escape_text_to_html(self, text):
        '''Try can convery plain text, maybe with some html markup into
        full html.
        Each line will be wrapped in a <p></p> tag, if needed
        '''

        # convert unicode characters to html
        _text = ""
        for ch in text:
            if ord(ch) >= 127:
                _text += "&#%d;" % ord(ch)
            else:
                _text += ch

        text = str(_text)

        # escape all special characters to they display correctly
        # unless they are already escaped
        for key, value in  ESCAPES.items():
            text = re.sub(r'([^\\]|^)%s' % key, r"\1%s" % value, text)

        # restore unicode chars
        # either &#DDD; or &#xDDD; have been escaped
        text = re.sub(r'\&amp;#([xX]?)(\d+);', r'&#\1\2;', text)

        # restore any html tags
        for tag in HTML_TAGS:
            for t in (tag, tag.upper()):
                text = re.sub(r'\&lt;(/?)%s\&gt;' % t, r'<\1%s>' % t, text)

        text = re.sub(r'\&amp;#[xX](\d+);', r'&#x\1;', text)

        # remove escaped chars
        for key, value in  ESCAPES.items():
            text = re.sub(r'\\%s' % key, r"%s" % value, text)

        # add paragraph tags
        paragraphs = []
        for line in text.splitlines():
            for tag in ('p', 'P', 'blockquote', 'BLOCKQUOTE'):
                if line.startswith('<%s>' % t) and line.endswith('</%s>' % t):
                    paragraphs.append(line)
                    break
            else:
                paragraphs.append("<p>%s</p>" % line)

        return paragraphs
#
