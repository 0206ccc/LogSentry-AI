@echo off
chcp 65001
echo ========================================
echo  LogSentry-AI Pro - Ollama本地模型安装脚本
echo ========================================
echo.

where ollama >nul 2>nul
if %errorlevel% neq 0 (
    echo [×] Ollama未安装，请先访问 https://ollama.com/download 下载安装
    pause
    exit /b 1
)

echo [√] Ollama已安装
echo.
echo 正在下载 qwen2:7b 模型（约4.4GB，请耐心等待）...
echo.

ollama pull qwen2:7b

if %errorlevel% neq 0 (
    echo [×] 模型下载失败，请检查网络
    pause
    exit /b 1
)

echo.
echo [√] 模型下载完成！
echo.
echo 使用方法：
echo 1. 在程序侧边栏选择"本地Ollama"
echo 2. API Key填任意值（如 ollama）
echo 3. 开始分析，数据完全本地处理
echo.
pause
