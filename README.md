# 🤖 企业级多智能体自闭环营销系统 (Enterprise Multi-Agent Workflow)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-State_Machine-orange)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B)
![RAG](https://img.shields.io/badge/RAG-ChromaDB-purple)

基于 **LangGraph** 状态机与 **RAG (检索增强生成)** 架构开发的企业级营销文案生成智能体。通过引入多智能体协同与“反思-重写”闭环，彻底解决大模型在商业落地中常见的“事实幻觉”与“风格不可控”问题。

> **🌟 核心升级说明：** > 本项目已从早期的线性单体 Prompt 脚本，彻底重构为**基于状态流转的 Multi-Agent 架构**，并实现了标准的前后端业务解耦。

---

## ✨ 核心特性 (Core Features)

* **🧠 多智能体协同与反思闭环 (Reflection & Multi-Agent)**
  抛弃传统的线性调用，采用 LangGraph 构建状态机。内置三大 Agent：
  * `Researcher`：负责知识检索与事实提取。
  * `Writer`：负责结合检索事实进行定向风格的初稿创作。
  * `Reviewer`：负责事实核查与合规审查，若发现幻觉参数，自动输出 Feedback 并打回 `Writer` 节点重写。
* **📚 深度 RAG 抗幻觉机制**
  集成 `ChromaDB` 向量库与 `m3e-base` 嵌入模型，构建企业私有知识库。所有生成的文案必须强制挂载真实技术参数，实现从根源上的数据防伪。
* **🛡️ 生产级防御性编程**
  针对大模型 JSON 格式化输出不稳定的通病，内置健壮的字符串清洗与反序列化解析模块，并通过 `.get()` 安全兜底机制保障服务端极高的容错率。
* **⚙️ 标准前后端分离交付**
  * **后端 (FastAPI)**：作为核心大模型推理与图计算引擎，提供高并发 RESTful API。
  * **前端 (Streamlit)**：轻量级数据驱动 Web 界面，实现平滑的用户交互。
  * **安全**：通过 `python-dotenv` 隔离真实 API 密钥，保障资产安全。

---

## 🗺️ 系统架构图 (Architecture)

系统采用 LangGraph 驱动的循环状态流转，最大重写次数（Iteration）阈值保护，防止 Token 无限消耗。

```text
[用户请求 (Topic & Tone)]
       │
       ▼
┌──────────────────┐
│  Researcher 节点 │ <--- 检索本地 ChromaDB 私有知识库
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│    Writer 节点   │ <--- 结合背景知识与风格要求，生成文案草稿
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   Reviewer 节点  │ <--- 严格审查：是否包含捏造数据？风格是否匹配？
└────────┬─────────┘
         │
         ├─── (审核不通过 / is_pass: False) ──> 返回 Feedback 并打回重写
         │
         ▼
[输出最终合规文案] (审核通过 或 达到最大循环次数)
📂 工程目录结构 (Directory Structure)
Plaintext
Enterprise-Marketing-Agent/
├── .env                  # 敏感环境变量配置 (需自行创建，切勿上传)
├── requirements.txt      # 项目依赖
├── data/
│   └── my_knowledge.txt  # 企业私有知识库文档 (RAG 数据源)
├── core/                 # Agent 核心大脑
│   ├── __init__.py
│   ├── state.py          # Agent 全局状态字典定义 (TypedDict & Reducer)
│   ├── nodes.py          # 检索、生成、审核三大核心节点逻辑
│   └── graph.py          # LangGraph 状态机边与条件路由编排
├── api/                  # 后端服务层
│   ├── __init__.py
│   └── server.py         # FastAPI 核心服务端 (端口: 8000)
└── web/                  # 前端展示层
    └── ui.py             # Streamlit 用户交互前端 (端口: 8501)
🚀 快速启动 (Quick Start)
1. 环境准备
Bash
# 克隆项目 (注意：请将下方链接替换为您 fork 后的仓库地址)
git clone [https://github.com/wxf-0251/Enterprise-Marketing-Agent.git](https://github.com/wxf-0251/Enterprise-Marketing-Agent.git)
cd Enterprise-Marketing-Agent

# 安装核心依赖
pip install -r requirements.txt
2. 配置密钥与本地环境
在项目根目录新建 .env 文件，并填入您的大模型 API 密钥（本项目默认使用 DeepSeek API）：

代码段
DEEPSEEK_API_KEY=your_api_key_here
HF_ENDPOINT=[https://hf-mirror.com](https://hf-mirror.com)  # 解决国内下载 HuggingFace 模型网络问题
3. 启动服务 (需开启两个终端)
终端 1：启动核心 Agent 后端引擎

Bash
uvicorn api.server:app --reload
启动成功后，后端将运行在 http://127.0.0.1:8000，并实时打印 Agent 节点的反思流转日志。

终端 2：启动前端交互页面

Bash
streamlit run web/ui.py
启动成功后，浏览器将自动打开 http://localhost:8501。

👨‍💻 开发者 (Author)
王秀蜂 - 独立架构与开发
