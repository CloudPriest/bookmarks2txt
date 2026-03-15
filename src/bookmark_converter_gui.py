#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
书签转换器 - PyQt5 GUI版本
将Chrome书签HTML文件转换为txt文件
"""

import os
import sys
import argparse
from html.parser import HTMLParser
from urllib.parse import urlparse
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QPushButton, QTextEdit,
                             QLineEdit, QFileDialog, QMessageBox, QGroupBox,
                             QProgressBar, QStatusBar, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QUrl, QTimer
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QFont, QDesktopServices


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


class ConversionThread(QThread):
    """转换线程，避免界面卡顿"""

    progress_signal = pyqtSignal(int)
    message_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(list, str, bool, str)  # links, output_path, success, error_msg

    def __init__(self, input_file, output_path):
        super().__init__()
        self.input_file = input_file
        self.output_path = output_path

    def run(self):
        try:
            self.message_signal.emit(f"正在解析书签文件: {self.input_file}")

            # 解析书签文件
            links = self.parse_bookmarks_file(self.input_file)

            if not links:
                self.finished_signal.emit([], self.output_path, False,
                                         "未找到任何书签链接。请确认文件是Chrome导出的书签HTML文件")
                return

            self.message_signal.emit(f"找到 {len(links)} 个书签，正在保存...")

            # 保存到txt文件
            self.save_to_txt(links, self.output_path)

            self.message_signal.emit(f"转换完成！文件已保存到: {self.output_path}")
            self.finished_signal.emit(links, self.output_path, True, "")

        except Exception as e:
            self.finished_signal.emit([], self.output_path, False, f"转换失败: {str(e)}")

    def parse_bookmarks_file(self, file_path):
        """解析书签HTML文件"""
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

    def save_to_txt(self, links, output_path):
        """将链接保存到txt文件"""
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


class DropLineEdit(QLineEdit):
    """支持拖放的文件路径输入框"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if os.path.isfile(file_path):
                self.setText(file_path)


class BookmarkConverterGUI(QMainWindow):
    """书签转换器主窗口"""

    def __init__(self):
        super().__init__()
        self.initUI()
        self.conversion_thread = None

    def initUI(self):
        """初始化用户界面"""
        self.setWindowTitle("书签转换器")
        self.setGeometry(300, 300, 450, 500)

        # 设置字体
        font = QFont()
        font.setPointSize(10)
        self.setFont(font)

        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 1. 输入文件选择区域
        input_group = QGroupBox("选择书签文件")
        input_layout = QVBoxLayout()

        # 拖放输入框
        self.input_path_edit = DropLineEdit()
        self.input_path_edit.setPlaceholderText("将书签HTML文件拖放到此处，或点击浏览按钮选择...")

        # 浏览按钮
        browse_layout = QHBoxLayout()
        self.browse_btn = QPushButton("浏览文件")
        self.browse_btn.clicked.connect(self.browse_input_file)
        browse_layout.addWidget(self.browse_btn)
        browse_layout.addStretch()

        input_layout.addWidget(QLabel("书签文件路径:"))
        input_layout.addWidget(self.input_path_edit)
        input_layout.addLayout(browse_layout)
        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)

        # 2. 输出路径选择区域
        output_group = QGroupBox("输出设置")
        output_layout = QVBoxLayout()

        # 输出路径显示和选择
        output_path_layout = QHBoxLayout()
        self.output_path_edit = QLineEdit()
        self.output_path_edit.setReadOnly(True)

        # 设置默认输出路径为桌面
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        if os.path.exists(desktop_path):
            default_output = os.path.join(desktop_path, "书签转换结果.txt")
            self.output_path_edit.setText(default_output)
        else:
            # 如果桌面不存在，使用当前目录
            default_output = os.path.join(os.getcwd(), "书签转换结果.txt")
            self.output_path_edit.setText(default_output)

        self.output_browse_btn = QPushButton("选择输出位置")
        self.output_browse_btn.clicked.connect(self.browse_output_file)
        output_path_layout.addWidget(QLabel("输出文件路径:"))
        output_path_layout.addWidget(self.output_path_edit, 1)
        output_path_layout.addWidget(self.output_browse_btn)

        # 打开文件夹按钮
        self.open_folder_btn = QPushButton("打开输出文件夹")
        self.open_folder_btn.clicked.connect(self.open_output_folder)
        self.open_folder_btn.setEnabled(True)

        output_layout.addLayout(output_path_layout)
        output_layout.addWidget(self.open_folder_btn)
        output_group.setLayout(output_layout)
        main_layout.addWidget(output_group)

        # 3. 转换按钮区域
        button_layout = QHBoxLayout()
        self.convert_btn = QPushButton("开始转换")
        self.convert_btn.clicked.connect(self.start_conversion)
        self.convert_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)

        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.clicked.connect(self.cancel_conversion)
        self.cancel_btn.setEnabled(False)

        button_layout.addStretch()
        button_layout.addWidget(self.convert_btn)
        button_layout.addWidget(self.cancel_btn)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        # 4. 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)

        # 5. 状态显示区域
        status_group = QGroupBox("转换状态")
        status_layout = QVBoxLayout()
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMaximumHeight(150)
        self.status_text.setPlaceholderText("状态信息将显示在这里...")
        status_layout.addWidget(self.status_text)
        status_group.setLayout(status_layout)
        main_layout.addWidget(status_group)

        # 6. 底部状态栏
        self.statusBar().showMessage("就绪")

        # 添加快捷键提示
        self.statusBar().showMessage("就绪 | 快捷键: Ctrl+O 打开文件 | Ctrl+S 选择输出 | Ctrl+R 打开文件夹")

        # 设置快捷键
        self.setup_shortcuts()

    def setup_shortcuts(self):
        """设置快捷键"""
        # Ctrl+O 打开文件
        self.browse_btn.setShortcut("Ctrl+O")
        # Ctrl+S 选择输出
        self.output_browse_btn.setShortcut("Ctrl+S")
        # Ctrl+R 打开文件夹
        self.open_folder_btn.setShortcut("Ctrl+R")

    def browse_input_file(self):
        """浏览输入文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择Chrome书签文件", "",
            "HTML文件 (*.html *.htm);;所有文件 (*.*)"
        )
        if file_path:
            self.input_path_edit.setText(file_path)
            self.statusBar().showMessage(f"已选择文件: {os.path.basename(file_path)}")

    def browse_output_file(self):
        """浏览输出文件"""
        # 获取当前输出路径或默认路径
        current_path = self.output_path_edit.text()
        if not current_path:
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            current_path = os.path.join(desktop_path, "书签转换结果.txt")

        file_path, _ = QFileDialog.getSaveFileName(
            self, "选择输出文件", current_path,
            "文本文件 (*.txt);;所有文件 (*.*)"
        )
        if file_path:
            self.output_path_edit.setText(file_path)
            self.statusBar().showMessage(f"输出文件已设置为: {os.path.basename(file_path)}")

    def open_output_folder(self):
        """打开输出文件所在文件夹"""
        output_path = self.output_path_edit.text()
        if output_path:
            folder_path = os.path.dirname(output_path)
            if os.path.exists(folder_path):
                QDesktopServices.openUrl(QUrl.fromLocalFile(folder_path))
                self.statusBar().showMessage(f"已打开文件夹: {folder_path}")
            else:
                QMessageBox.warning(self, "警告", f"文件夹不存在: {folder_path}")
        else:
            QMessageBox.warning(self, "警告", "请先设置输出文件路径")

    def start_conversion(self):
        """开始转换"""
        # 获取输入文件路径
        input_file = self.input_path_edit.text().strip()
        if not input_file:
            QMessageBox.warning(self, "警告", "请选择书签文件")
            return

        if not os.path.exists(input_file):
            QMessageBox.warning(self, "警告", f"文件不存在: {input_file}")
            return

        # 获取输出文件路径
        output_file = self.output_path_edit.text().strip()
        if not output_file:
            QMessageBox.warning(self, "警告", "请设置输出文件路径")
            return

        # 检查输出目录是否存在
        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except Exception as e:
                QMessageBox.warning(self, "警告", f"无法创建输出目录: {str(e)}")
                return

        # 更新UI状态
        self.convert_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.browse_btn.setEnabled(False)
        self.output_browse_btn.setEnabled(False)
        self.open_folder_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        # 清空状态文本
        self.status_text.clear()
        self.append_status("开始转换...")

        # 创建并启动转换线程
        self.conversion_thread = ConversionThread(input_file, output_file)
        self.conversion_thread.message_signal.connect(self.append_status)
        self.conversion_thread.finished_signal.connect(self.conversion_finished)
        self.conversion_thread.start()

        self.statusBar().showMessage("正在转换...")

    def cancel_conversion(self):
        """取消转换"""
        if self.conversion_thread and self.conversion_thread.isRunning():
            self.conversion_thread.terminate()
            self.conversion_thread.wait()
            self.append_status("转换已取消")
            self.reset_ui_state()
            self.statusBar().showMessage("转换已取消")

    def conversion_finished(self, links, output_path, success, error_msg):
        """转换完成回调"""
        if success:
            self.progress_bar.setValue(100)
            self.append_status(f"✓ 转换成功！")
            self.append_status(f"✓ 找到 {len(links)} 个书签")
            self.append_status(f"✓ 文件已保存到: {output_path}")

            # 询问是否打开输出文件夹
            reply = QMessageBox.question(
                self, "转换完成",
                f"转换成功！共找到 {len(links)} 个书签。\n文件已保存到:\n{output_path}\n\n是否打开输出文件夹？",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes
            )

            if reply == QMessageBox.Yes:
                self.open_output_folder()

            self.statusBar().showMessage("转换完成")
        else:
            self.append_status(f"✗ 转换失败: {error_msg}")
            QMessageBox.critical(self, "转换失败", error_msg)
            self.statusBar().showMessage("转换失败")

        self.reset_ui_state()

    def append_status(self, message):
        """添加状态消息"""
        self.status_text.append(message)
        # 滚动到底部
        self.status_text.verticalScrollBar().setValue(
            self.status_text.verticalScrollBar().maximum()
        )

    def reset_ui_state(self):
        """重置UI状态"""
        self.convert_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.browse_btn.setEnabled(True)
        self.output_browse_btn.setEnabled(True)
        self.open_folder_btn.setEnabled(True)

        # 延迟隐藏进度条
        QTimer.singleShot(2000, lambda: self.progress_bar.setVisible(False))

    def closeEvent(self, event):
        """关闭窗口事件"""
        if self.conversion_thread and self.conversion_thread.isRunning():
            reply = QMessageBox.question(
                self, "确认退出",
                "转换正在进行中，确定要退出吗？",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                self.conversion_thread.terminate()
                self.conversion_thread.wait()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


def main():
    """主函数"""
    app = QApplication(sys.argv)
    app.setApplicationName("书签转换器")
    app.setOrganizationName("BookmarkConverter")

    # 设置应用程序样式
    app.setStyle('Fusion')

    # 创建并显示主窗口
    window = BookmarkConverterGUI()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()