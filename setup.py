#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
书签转换器安装脚本
"""

from setuptools import setup, find_packages
import os

# 读取 README 文件
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# 读取版本信息
with open('src/__init__.py', 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.split('=')[1].strip().strip("'\"")
            break
    else:
        version = '1.0.0'

setup(
    name='bookmark-converter',
    version=version,
    description='将 Chrome 书签 HTML 文件转换为文本文件的工具',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='书签转换器作者',
    author_email='your-email@example.com',
    url='https://github.com/yourusername/bookmark-converter',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'PyQt5>=5.15.0',
    ],
    entry_points={
        'console_scripts': [
            'bookmark-converter-cli=chrome_bookmarks_to_txt:main',
        ],
        'gui_scripts': [
            'bookmark-converter=bookmark_converter_gui:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
    ],
    python_requires='>=3.6',
    keywords='bookmark, converter, chrome, html, txt, utility',
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/bookmark-converter/issues',
        'Source': 'https://github.com/yourusername/bookmark-converter',
    },
)