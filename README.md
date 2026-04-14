#  轻量级多智能体营销文案生成器 (PoC)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-State_Machine-orange)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)

这是一个基于 **LangGraph** 和 **RAG** 的多智能体协作项目，主要用于自动生成特定风格的营销文案（如小红书风）。

>  开发小记：
> 作为一名机器人工程专业的学生，我最初只是写了一个简单的 LangChain 线性调用脚本来生成文案。但在测试中发现，大模型在遇到具体的“硬核产品参数”时特别喜欢胡编乱造。为了约束它的输出，我重构了整个架构，引入了本地 RAG 来提供真实依据，并用 LangGraph 把流程改造成了“生成 -> 审核 -> 打回重写”的闭环状态机。踩了不少坑，但也算把流程跑通了。

---

##  遇到过的问题与解决方案 (Features)

* **痛点 1：大模型总是捏造产品参数（幻觉）**
  * **方案：** 接入 `ChromaDB` 和 `m3e-base` 构建了一个非常轻量级的本地知识库 (RAG)。Agent 在写文案前，必须先去知识库里检索真实数据，强制根据检索结果生成。
* **痛点 2：输出风格不稳定，一次生成往往不能用**
  * **方案：** 抛弃单次请求，引入 LangGraph 构建状态机。设定了 `Researcher`, `Writer`, `Reviewer` 三个节点。写完后先过 `Reviewer` 审核，一旦发现捏造数据或风格不对，直接打回 `Writer` 重新生成，最多循环 3 次。
* **痛点 3：模型 JSON 输出不稳定，导致后端经常崩**
  * **方案：** 测试时发现部分模型（如 DeepSeek）对强约束的 `json_schema` 语法兼容不好，会报 400 错误。因此改用“手写 Prompt 约束 + 后端健壮的反序列化清洗”，并加了 `.get()` 兜底机制，保证后端服务不会因为大模型一次抽风就彻底死掉。
* **痛点 4：单体脚本不好扩展**
  * **方案：** 做了基础的前后端分离。FastAPI 跑后端计算，Streamlit 做前端可视化，并用 `.env` 彻底隔离了 API Key 保护资产安全。

---

##  系统流转逻辑

```text
[输入主题与风格] -> 检索本地 ChromaDB -> Writer 写初稿 -> Reviewer 审核
                                                     │
                                 (不合格返回重写) ───┘
                                                     │
                                             [输出最终文案]
```

---

##  核心目录结构

```text
Enterprise-Marketing-Agent/
├── .env                  # 记得自己建一个，放 API Key
├── requirements.txt      
├── data/
│   └── my_knowledge.txt  # RAG 的本地测试语料
├── core/                 # Agent 核心逻辑
│   ├── state.py          # 全局状态定义
│   ├── nodes.py          # 检索、生成、审核的节点代码
│   └── graph.py          # LangGraph 图流转编排
├── api/                  
│   └── server.py         # FastAPI 接口 (端口 8000)
└── web/                  
    └── ui.py             # Streamlit 前端 (端口 8501)
```

---

##  跑起来试试 (Quick Start)

### 1. 环境准备
```bash
git clone https://github.com/wxf-0251/Enterprise-Marketing-Agent.git
cd Enterprise-Marketing-Agent
pip install -r requirements.txt
```

### 2. 配置环境
在根目录新建一个 `.env` 文件，填入你的大模型 API 密钥（测试时使用的是 DeepSeek）：
```env
DEEPSEEK_API_KEY=你的密钥
HF_ENDPOINT=https://hf-mirror.com  # 解决国内加载 HuggingFace m3e 模型卡死的问题
TOKENIZERS_PARALLELISM=false       # 核心修复：防止 Windows 下多进程分词产生死锁
```

### 3. 分别启动前后端

**终端 1：启动后台服务**
```bash
uvicorn api.server:app --reload
```

**终端 2：启动前端页面**
```bash
streamlit run web/ui.py
```

---

