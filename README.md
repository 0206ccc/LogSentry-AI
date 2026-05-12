# 🔍 LogSentry-AI Pro

AI智能安全日志分析工具 - 专业版

## ✨ 功能特性

| 功能 | 说明 |
|------|------|
| 🤖 AI攻击识别 | 基于大语言模型，自动识别OWASP Top 10攻击 |
| 🌍 IP情报查询 | 自动查询攻击IP归属地、ISP信息 |
| 🛡️ WAF规则生成 | 根据攻击类型自动生成ModSecurity防御规则 |
| 📁 实时监控 | 监控日志目录，新文件自动分析 |
| 💻 本地模型 | 支持Ollama本地部署，保护数据隐私 |
| 📊 可视化报告 | 统计面板、攻击分布、详细表格、CSV导出 |

## 🚀 快速开始

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 🔧 配置说明

### 云端API（推荐新手）
1. **通义千问**：访问 [阿里云百炼](https://bailian.console.aliyun.com) 申请API Key
2. **DeepSeek**：访问 [DeepSeek平台](https://platform.deepseek.com) 申请API Key

### 本地模型（推荐隐私场景）
1. 安装 [Ollama](https://ollama.com/download)
2. 下载模型：`ollama pull qwen2:7b`
3. 选择"本地Ollama"即可离线运行

## 📖 使用指南

1. 在侧边栏选择API提供商并配置Key
2. 上传Nginx/Apache日志文件（.log/.txt）
3. 点击"开始AI分析"
4. 查看统计面板、攻击分布、详细结果
5. 导出CSV报告或复制WAF规则

## 🛣️ 技术架构

```
LogSentry-AI Pro
├── 日志解析层    → Nginx/Apache格式解析
├── AI分析层      → LLM攻击识别（云端/本地）
├── 情报查询层    → IP归属地、ISP查询
├── 规则生成层    → WAF防御规则自动生成
├── 监控层        → 目录实时监控
└── 展示层        → Streamlit可视化界面
```

## 📜 许可证

MIT License
