@echo off
chcp 65001 >nul
echo 正在启动书签转换器...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.6+
    pause
    exit /b 1
)

REM 检查PyQt5是否安装
python -c "import PyQt5" >nul 2>&1
if errorlevel 1 (
    echo 检测到PyQt5未安装，正在安装...
    echo 请稍候...
    pip install PyQt5
    if errorlevel 1 (
        echo 安装PyQt5失败，请手动安装: pip install PyQt5
        pause
        exit /b 1
    )
    echo PyQt5安装成功!
    echo.
)

REM 运行书签转换器
echo 启动书签转换器...
python bookmark_converter_gui.py

if errorlevel 1 (
    echo.
    echo 程序运行出错，请检查错误信息
    pause
)