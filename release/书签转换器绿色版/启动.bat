@echo off
chcp 65001 >nul
title 书签转换器绿色版
echo ========================================
echo     书签转换器绿色版 v1.0.0
echo ========================================
echo.
echo 正在启动书签转换器...
echo.
echo 使用说明：
echo 1. 将 Chrome 书签 HTML 文件拖放到程序窗口
echo 2. 点击"开始转换"按钮
echo 3. 结果将保存到桌面
echo.
echo 按任意键启动程序...
pause >nul
start "" "书签转换器.exe"
exit