# 📕 小红书爆款文案生成 Agent (PoC)

基于 LangChain 与大语言模型 (LLM) 开发的小红书爆款文案生成与分析辅助工具。
**【最新更新】** 项目已重构为前后端分离架构，新增 FastAPI 服务端，支持将 Agent 工作流作为标准 RESTful API 提供给第三方业务调用。

## ✨ 核心特性

- **前后端分离架构**：提供 Streamlit 可视化 Web UI 与 FastAPI 标准接口两种使用形态。
- **高度模块化的 Prompt 设计**：结构化输出（标题推荐+痛点引入+干货正文+互动引导）。
- **多风格一键切换**：支持“干货科普、闺蜜种草、搞笑幽默”等多模态情绪输出。
- **企业级安全规范**：引入‘dotenv’进行敏感环境变量隔离，保护 API 资产安全。
- **低耦合架构**：使用 LangChain 的 LCEL 语法构建工作流，可无缝平替不同底层大模型（支持 DeepSeek, Qwen, OpenAI 等）。

## 🛠️ 技术栈

- **核心框架**: Python 3.10+
- **AI 编排**: LangChain (核心逻辑与大模型编排)
- **后端接口**: FastAPI + Uvicorn + Pydantic (高并发 RESTful API 封装)
- **前端交互**: Streamlit (轻量级数据驱动 Web 界面)
- **安全配置**: python-dotenv

## 🚀 快速启动

### 1. 克隆项目与安装依赖
```bash
git clone [https://github.com/wxf-0251/XiaoHongShu-Copy-Agent-PoC.git](https://github.com/wxf-0251/XiaoHongShu-Copy-Agent-PoC.git)
cd XiaoHongShu-Copy-Agent-PoC
pip install -r requirements.txt
