#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chrome书签转txt文件程序
将Chrome导出的书签HTML文件转换为txt文件
输出格式：
第一部分：纯链接列表（每行一个）
第二部分：链接+名称（格式：名称 - 链接）
"""

import os
import sys
import argparse
from html.parser import HTMLParser
from urllib.parse import urlparse


class ChromeBookmarkParser(HTMLParser):
    """解析Chrome书签HTML文件"""

    def __init__(self):
        super().__init__()
        self.links = []  # 存储(链接, 名称)元组
        self.in_a_tag = False
        self.current_link = None
        self.current_name = ""

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'a':
            self.in_a_tag = True
            # 查找href属性
            href = None
            for attr, value in attrs:
                if attr.lower() == 'href':
                    href = value
                    break

            if href:
                self.current_link = href
                self.current_name = ""  # 重置名称

    def handle_endtag(self, tag):
        if tag.lower() == 'a' and self.in_a_tag:
            self.in_a_tag = False
            if self.current_link and self.current_name:
                # 添加到列表
                self.links.append((self.current_link, self.current_name.strip()))
                self.current_link = None
                self.current_name = ""

    def handle_data(self, data):
        if self.in_a_tag and self.current_link:
            self.current_name += data


def parse_bookmarks_file(file_path):
    """
    解析书签HTML文件

    Args:
        file_path: 书签HTML文件路径

    Returns:
        list: (链接, 名称)元组列表
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # 尝试其他编码
        with open(file_path, 'r', encoding='gbk', errors='ignore') as f:
            content = f.read()

    parser = ChromeBookmarkParser()
    parser.feed(content)
    return parser.links


def save_to_txt(links, output_path):
    """
    将链接保存到txt文件

    Args:
        links: (链接, 名称)元组列表
        output_path: 输出文件路径
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            # 第一部分：纯链接
            f.write("=" * 50 + "\n")
            f.write("第一部分：纯链接列表\n")
            f.write("=" * 50 + "\n\n")

            for link, name in links:
                f.write(f"{link}\n")

            f.write("\n\n" + "=" * 50 + "\n")
            f.write("第二部分：详细书签列表\n")
            f.write("=" * 50 + "\n\n")

            for i, (link, name) in enumerate(links, 1):
                f.write(f"{i}\n")
                f.write(f"{name}\n")
                f.write(f"{link}\n")
                f.write("\n")

        print(f"成功保存到: {output_path}")
        print(f"总共处理了 {len(links)} 个书签")

    except Exception as e:
        print(f"保存文件时出错: {e}")
        sys.exit(1)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='将Chrome书签HTML文件转换为txt文件',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  %(prog)s bookmarks.html
  %(prog)s bookmarks.html -o output.txt
  %(prog)s -i bookmarks.html -o my_links.txt

书签文件获取方法:
  1. 在Chrome中打开书签管理器 (Ctrl+Shift+O)
  2. 点击右上角三个点 -> "导出书签"
  3. 保存为HTML文件
        """
    )

    parser.add_argument('input_file', nargs='?', help='Chrome书签HTML文件路径')
    parser.add_argument('-i', '--input', help='输入文件路径')
    parser.add_argument('-o', '--output', help='输出文件路径（默认：书签文件名.txt）')

    args = parser.parse_args()

    # 确定输入文件
    input_file = args.input if args.input else args.input_file

    if not input_file:
        print("错误: 请指定书签HTML文件路径")
        print("使用方法: python chrome_bookmarks_to_txt.py <书签文件>")
        sys.exit(1)

    # 检查文件是否存在
    if not os.path.exists(input_file):
        print(f"错误: 文件不存在: {input_file}")
        sys.exit(1)

    # 确定输出文件
    if args.output:
        output_file = args.output
    else:
        # 使用输入文件名，扩展名改为.txt
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = f"{base_name}_links.txt"

    print(f"正在解析书签文件: {input_file}")

    # 解析书签文件
    links = parse_bookmarks_file(input_file)

    if not links:
        print("错误: 未找到任何书签链接")
        print("请确认文件是Chrome导出的书签HTML文件")
        print("Chrome书签HTML文件通常包含 <DT><A HREF=\"...\">名称</A> 格式的链接")
        sys.exit(1)

    # 保存到txt文件
    save_to_txt(links, output_file)


if __name__ == "__main__":
    main()