# XiaoHongShu-Copy-Agent-PoC
基于 LangChain 开发的小红书文案快速生成与风格迁移 Agent
# 📕 新媒体智能营销文案 Agent (PoC)

基于 LangChain 与大语言模型（LLM）开发的小红书爆款文案生成与分析辅助工具。用于快速验证 AI 产品概念（PoC），旨在解决新媒体运营中内容产出效率低、风格难以统一的痛点。

## ✨ 核心特性
- **高度模块化的 Prompt 设计**：结构化输出（标题推荐+痛点引入+干货正文+互动引导）。
- **多风格一键切换**：支持“干货科普、闺蜜种草、搞笑幽默”等多模态情绪输出。
- **现代化前端交互**：基于 Streamlit 快速构建数据驱动的轻量级 Web 界面。
- **低耦合架构**：使用 LangChain 的 LCEL 语法构建工作流，可无缝平替不同底层大模型（支持 OpenAI, DeepSeek, GLM 等）。

## 🛠️ 技术栈
- Python 3.10+
- [LangChain](https://github.com/langchain-ai/langchain) (核心逻辑与大模型编排)
- [Streamlit](https://streamlit.io/) (前端快速原型 UI)
- LLM API (兼容 OpenAI 接口)

## 📸 运行截图


## 🚀 快速启动
1. 克隆项目到本地
2. 安装依赖：`pip install streamlit langchain langchain-openai langchain-core`
3. 运行项目：`streamlit run app.py`
4. 在网页左侧填入你的大模型 API Key 即可开始使用。
