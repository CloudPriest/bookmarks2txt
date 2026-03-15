# 使用说明

## 快速开始

### 对于普通用户（使用绿色软件）

1. 从 Releases 页面下载 `书签转换器.exe`
2. 双击运行 `书签转换器.exe`
3. 按照界面提示选择书签文件并开始转换

### 对于开发者（使用源代码）

1. 安装 Python 3.6+ 和 PyQt5：
   ```bash
   pip install PyQt5
   ```
2. 运行程序：
   ```bash
   python src/bookmark_converter_gui.py
   ```

## 详细步骤

### 1. 获取 Chrome 书签文件

1. 打开 Google Chrome 浏览器
2. 按下 `Ctrl+Shift+O` 打开书签管理器
3. 点击右上角的三个点菜单 (⋮)
4. 选择"导出书签"
5. 将文件保存为 HTML 格式（例如：`bookmarks.html`）

### 2. 运行书签转换器

#### 图形界面版本
1. 启动书签转换器
2. 将书签 HTML 文件拖放到输入框，或点击"浏览文件"按钮选择
3. 确认输出文件路径（默认保存在桌面）
4. 点击"开始转换"按钮
5. 等待转换完成
6. 可点击"打开输出文件夹"查看转换结果

#### 命令行版本
```bash
# 基本用法
python src/chrome_bookmarks_to_txt.py bookmarks.html

# 指定输出文件
python src/chrome_bookmarks_to_txt.py bookmarks.html -o my_links.txt

# 使用相对路径
python src/chrome_bookmarks_to_txt.py ../downloads/bookmarks.html

# 查看帮助信息
python src/chrome_bookmarks_to_txt.py -h
```

### 3. 查看转换结果

转换后的文本文件包含两部分：

#### 第一部分：纯链接列表
适合用于批量处理、脚本导入等场景。

#### 第二部分：详细书签列表
包含序号、名称和链接，便于阅读和管理。

## 快捷键

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+O` | 打开文件选择对话框 |
| `Ctrl+S` | 选择输出文件路径 |
| `Ctrl+R` | 打开输出文件夹 |
| `Esc` | 关闭窗口（某些情况下） |

## 常见问题

### Q: 转换时提示"未找到任何书签链接"
**A**: 请确认：
1. 文件是 Chrome 导出的书签 HTML 文件
2. 文件包含有效的书签链接（格式为 `<DT><A HREF="...">名称</A>`）
3. 文件编码正确（程序支持 UTF-8 和 GBK 编码）

### Q: 程序运行缓慢或卡住
**A**:
1. 书签文件过大时可能需要较长时间处理
2. 确保有足够的内存
3. 可以尝试使用命令行版本处理大文件

### Q: 如何批量转换多个书签文件？
**A**: 可以使用命令行版本配合脚本：
```bash
# Windows 批处理示例
for %%f in (*.html) do (
    python src/chrome_bookmarks_to_txt.py "%%f" -o "output_%%~nf.txt"
)
```

### Q: 支持其他浏览器的书签文件吗？
**A**: 目前主要支持 Chrome 导出的书签格式。其他浏览器（如 Firefox、Edge）的书签格式可能类似，但不保证完全兼容。

## 高级用法

### 集成到其他程序
```python
import sys
sys.path.append('path/to/bookmark-converter/src')

from chrome_bookmarks_to_txt import parse_bookmarks_file, save_to_txt

# 解析书签文件
links = parse_bookmarks_file('bookmarks.html')

# 自定义处理
filtered_links = [(url, name) for url, name in links if 'github' in url]

# 保存结果
save_to_txt(filtered_links, 'filtered_links.txt')
```

### 自定义输出格式
修改 `src/bookmark_converter_gui.py` 中的 `save_to_txt` 函数来自定义输出格式。

## 故障排除

### 错误：ModuleNotFoundError: No module named 'PyQt5'
**解决**：安装 PyQt5
```bash
pip install PyQt5
```

### 错误：程序闪退
**解决**：
1. 检查 Python 版本（需要 Python 3.6+）
2. 检查系统是否满足要求
3. 尝试以管理员身份运行
4. 查看日志文件（如果存在）

### 错误：编码问题
**解决**：
1. 尝试将书签文件用记事本打开
2. 选择"另存为"，编码选择"UTF-8"
3. 使用保存后的文件进行转换

## 联系支持

如有其他问题，请：
1. 查看 [GitHub Issues](https://github.com/yourusername/bookmark-converter/issues)
2. 提交新的 Issue
3. 或发送邮件至 your-email@example.com