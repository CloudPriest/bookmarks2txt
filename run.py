#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
书签转换器运行入口
可以直接从项目根目录运行: python run.py
"""

import sys
import os

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    # 导入并运行 GUI 版本
    from bookmark_converter_gui import main
    main()