#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
书签转换器打包脚本
用于将 Python 程序打包为可执行文件
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path

# 项目根目录
ROOT_DIR = Path(__file__).parent
SRC_DIR = ROOT_DIR / 'src'
DIST_DIR = ROOT_DIR / 'dist'
BUILD_DIR = ROOT_DIR / 'build'
SPEC_DIR = ROOT_DIR / 'spec'

# 确保目录存在
DIST_DIR.mkdir(exist_ok=True)
BUILD_DIR.mkdir(exist_ok=True)
SPEC_DIR.mkdir(exist_ok=True)


def clean_build():
    """清理构建目录"""
    print("清理构建目录...")
    for dir_path in [BUILD_DIR, DIST_DIR, SPEC_DIR]:
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"  已删除: {dir_path}")

    # 删除 .spec 文件
    for spec_file in ROOT_DIR.glob("*.spec"):
        spec_file.unlink()
        print(f"  已删除: {spec_file}")


def build_gui_version():
    """构建 GUI 版本"""
    print("\n构建 GUI 版本...")

    gui_script = SRC_DIR / 'bookmark_converter_gui.py'

    if not gui_script.exists():
        print(f"错误: 找不到 GUI 脚本: {gui_script}")
        return False

    # PyInstaller 命令
    cmd = [
        'pyinstaller',
        '--name=书签转换器',
        '--windowed',  # 不显示控制台窗口
        '--onedir',    # 单目录模式（更容易调试）
        '--clean',     # 清理临时文件
        '--noconfirm', # 不确认覆盖
        f'--distpath={DIST_DIR}',
        f'--workpath={BUILD_DIR}',
        f'--specpath={SPEC_DIR}',
        # '--add-data=examples;examples',  # 包含示例文件（可选）
        '--icon=NONE',  # 暂时不使用图标
        '--hidden-import=PyQt5.sip',
        '--hidden-import=html.parser',
        '--hidden-import=urllib.parse',
        '--collect-all=PyQt5',
        str(gui_script)
    ]

    print(f"执行命令: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("构建成功!")
        print(f"输出目录: {DIST_DIR / '书签转换器'}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"构建失败: {e}")
        print(f"标准错误: {e.stderr}")
        return False


def build_cli_version():
    """构建命令行版本"""
    print("\n构建命令行版本...")

    cli_script = SRC_DIR / 'chrome_bookmarks_to_txt.py'

    if not cli_script.exists():
        print(f"错误: 找不到 CLI 脚本: {cli_script}")
        return False

    # PyInstaller 命令
    cmd = [
        'pyinstaller',
        '--name=书签转换器CLI',
        '--console',   # 显示控制台窗口
        '--onedir',    # 单目录模式
        '--clean',
        '--noconfirm',
        f'--distpath={DIST_DIR}',
        f'--workpath={BUILD_DIR}',
        f'--specpath={SPEC_DIR}',
        '--hidden-import=html.parser',
        '--hidden-import=urllib.parse',
        str(cli_script)
    ]

    print(f"执行命令: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("构建成功!")
        print(f"输出目录: {DIST_DIR / '书签转换器CLI'}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"构建失败: {e}")
        print(f"标准错误: {e.stderr}")
        return False


def build_single_exe():
    """构建单个可执行文件（便携版）"""
    print("\n构建单个可执行文件版本...")

    gui_script = SRC_DIR / 'bookmark_converter_gui.py'

    if not gui_script.exists():
        print(f"错误: 找不到 GUI 脚本: {gui_script}")
        return False

    # PyInstaller 命令 - 单文件模式
    cmd = [
        'pyinstaller',
        '--name=书签转换器',
        '--windowed',
        '--onefile',   # 单文件模式
        '--clean',
        '--noconfirm',
        f'--distpath={DIST_DIR}',
        f'--workpath={BUILD_DIR}',
        f'--specpath={SPEC_DIR}',
        # '--add-data=examples;examples',  # 包含示例文件（可选）
        '--icon=NONE',
        '--hidden-import=PyQt5.sip',
        '--hidden-import=html.parser',
        '--hidden-import=urllib.parse',
        '--collect-all=PyQt5',
        str(gui_script)
    ]

    print(f"执行命令: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("构建成功!")
        exe_path = DIST_DIR / '书签转换器.exe'
        if exe_path.exists():
            print(f"可执行文件: {exe_path}")
            print(f"文件大小: {exe_path.stat().st_size / 1024 / 1024:.2f} MB")
        return True
    except subprocess.CalledProcessError as e:
        print(f"构建失败: {e}")
        print(f"标准错误: {e.stderr}")
        return False


def create_portable_package():
    """创建便携版包"""
    print("\n创建便携版包...")

    # 单文件版本路径
    exe_file = DIST_DIR / '书签转换器.exe'
    portable_dir = DIST_DIR / '书签转换器便携版'

    if not exe_file.exists():
        print(f"错误: 找不到可执行文件: {exe_file}")
        return False

    # 创建便携版目录
    portable_dir.mkdir(exist_ok=True)

    # 复制文件
    files_to_copy = [
        (exe_file, portable_dir / '书签转换器.exe'),
        (ROOT_DIR / 'README.md', portable_dir / 'README.md'),
        (ROOT_DIR / 'LICENSE', portable_dir / 'LICENSE'),
        (ROOT_DIR / 'examples', portable_dir / 'examples'),
        (ROOT_DIR / 'docs', portable_dir / 'docs'),
    ]

    for src, dst in files_to_copy:
        if src.exists():
            if src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
            print(f"  已复制: {src.name}")

    # 创建启动脚本
    bat_content = '''@echo off
chcp 65001 >nul
echo 书签转换器便携版
echo 版本 1.0.0
echo.
echo 正在启动...
start "" "书签转换器.exe"
'''

    bat_file = portable_dir / '启动书签转换器.bat'
    bat_file.write_text(bat_content, encoding='utf-8')
    print(f"  已创建: {bat_file.name}")

    print(f"便携版已创建: {portable_dir}")
    return True


def create_release_zip():
    """创建发布 ZIP 包"""
    print("\n创建发布 ZIP 包...")

    import zipfile
    import datetime

    # 版本号
    version = '1.0.0'
    date_str = datetime.datetime.now().strftime('%Y%m%d')

    # ZIP 文件名
    zip_name = f'书签转换器_v{version}_{date_str}.zip'
    zip_path = DIST_DIR / zip_name

    # 要包含的文件和目录
    items_to_zip = [
        DIST_DIR / '书签转换器便携版',
        DIST_DIR / '书签转换器.exe',
        ROOT_DIR / 'README.md',
        ROOT_DIR / 'LICENSE',
        ROOT_DIR / 'examples',
        ROOT_DIR / 'docs',
    ]

    # 过滤掉不存在的项目
    items_to_zip = [item for item in items_to_zip if item.exists()]

    if not items_to_zip:
        print("错误: 没有找到要打包的文件")
        return False

    print(f"创建 ZIP 文件: {zip_path}")

    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for item in items_to_zip:
                if item.is_file():
                    # 添加单个文件
                    arcname = item.relative_to(ROOT_DIR) if item.is_relative_to(ROOT_DIR) else item.name
                    zipf.write(item, arcname)
                    print(f"  已添加文件: {arcname}")
                elif item.is_dir():
                    # 添加整个目录
                    for root, dirs, files in os.walk(item):
                        for file in files:
                            file_path = Path(root) / file
                            arcname = file_path.relative_to(ROOT_DIR) if file_path.is_relative_to(ROOT_DIR) else file_path.relative_to(item.parent)
                            zipf.write(file_path, arcname)
                    print(f"  已添加目录: {item.name}")

        # 显示 ZIP 文件信息
        zip_size = zip_path.stat().st_size / 1024 / 1024
        print(f"ZIP 文件大小: {zip_size:.2f} MB")
        print(f"ZIP 文件路径: {zip_path}")

        return True
    except Exception as e:
        print(f"创建 ZIP 失败: {e}")
        return False


def main():
    """主函数"""
    print("=" * 50)
    print("书签转换器打包工具")
    print("=" * 50)

    # 检查操作系统
    if platform.system() != 'Windows':
        print("警告: 本工具主要针对 Windows 系统优化")
        print("在其他系统上可能需要调整参数")

    # 清理旧的构建文件
    clean_build()

    # 构建不同版本
    build_success = True

    # 构建单文件版本（便携版）
    if not build_single_exe():
        build_success = False
        print("单文件版本构建失败，尝试构建目录版本...")
        if not build_gui_version():
            build_success = False

    # 构建命令行版本（可选）
    # if build_success:
    #     build_cli_version()

    # 创建便携版包
    if build_success:
        create_portable_package()

    # 创建发布 ZIP
    if build_success:
        create_release_zip()

    print("\n" + "=" * 50)
    if build_success:
        print("打包完成!")
        print(f"输出目录: {DIST_DIR}")
        print("\n生成的文件:")
        for item in DIST_DIR.iterdir():
            if item.is_dir():
                print(f"  📁 {item.name}/")
            else:
                size = item.stat().st_size
                size_str = f"{size/1024/1024:.1f}MB" if size > 1024*1024 else f"{size/1024:.1f}KB"
                print(f"  📄 {item.name} ({size_str})")
    else:
        print("打包过程中出现错误!")

    return 0 if build_success else 1


if __name__ == "__main__":
    sys.exit(main())