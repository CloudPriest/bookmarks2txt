#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试书签解析器
"""

import os
import sys
import tempfile
import unittest

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from bookmark_converter_gui import ChromeBookmarkParser


class TestChromeBookmarkParser(unittest.TestCase):
    """测试 Chrome 书签解析器"""

    def test_parser_basic(self):
        """测试基本解析功能"""
        html_content = '''<!DOCTYPE NETSCAPE-Bookmark-file-1>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>
    <DT><A HREF="https://www.google.com/">Google</A>
    <DT><A HREF="https://www.github.com/">GitHub</A>
</DL>'''

        parser = ChromeBookmarkParser()
        parser.feed(html_content)

        self.assertEqual(len(parser.links), 2)
        self.assertEqual(parser.links[0], ("https://www.google.com/", "Google"))
        self.assertEqual(parser.links[1], ("https://www.github.com/", "GitHub"))

    def test_parser_with_special_chars(self):
        """测试特殊字符"""
        html_content = '''<!DOCTYPE NETSCAPE-Bookmark-file-1>
<TITLE>Bookmarks</TITLE>
<DL><p>
    <DT><A HREF="https://example.com/test%20page.html">测试 页面</A>
</DL>'''

        parser = ChromeBookmarkParser()
        parser.feed(html_content)

        self.assertEqual(len(parser.links), 1)
        self.assertEqual(parser.links[0], ("https://example.com/test%20page.html", "测试 页面"))

    def test_parser_empty(self):
        """测试空内容"""
        html_content = '''<!DOCTYPE NETSCAPE-Bookmark-file-1>
<TITLE>Bookmarks</TITLE>
<DL><p>
</DL>'''

        parser = ChromeBookmarkParser()
        parser.feed(html_content)

        self.assertEqual(len(parser.links), 0)

    def test_parser_multiline(self):
        """测试多行内容"""
        html_content = '''<!DOCTYPE NETSCAPE-Bookmark-file-1>
<TITLE>Bookmarks</TITLE>
<DL><p>
    <DT><A HREF="https://www.python.org/">
        Python Programming Language
    </A>
</DL>'''

        parser = ChromeBookmarkParser()
        parser.feed(html_content)

        self.assertEqual(len(parser.links), 1)
        self.assertEqual(parser.links[0], ("https://www.python.org/", "Python Programming Language"))


if __name__ == '__main__':
    unittest.main()