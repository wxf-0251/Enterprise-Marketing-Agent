import json
import os
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from pydantic import BaseModel, Field
from .state import AgentState

llm = ChatOpenAI(
    openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
    openai_api_base="https://api.deepseek.com/v1",
    model_name="deepseek-chat"
)

embeddings = HuggingFaceEmbeddings(model_name="moka-ai/m3e-base")
vector_db = Chroma(persist_directory="./chroma_db_ollama", embedding_function=embeddings)
retriever = vector_db.as_retriever(search_kwargs={"k": 2})

def retrieve_knowledge(state: AgentState) -> dict:
    docs = retriever.invoke(state["topic"])
    context_text = "\n".join([doc.page_content for doc in docs])
    return {"context": context_text}

def generate_draft(state: AgentState) -> dict:
    if state.get("iteration", 0) == 0:
        prompt = f"请以【{state['tone']}】写关于【{state['topic']}】的小红书文案。\n参考以下事实（不可捏造）：\n{state['context']}"
    else:
        prompt = f"请修改文案。\n原稿：{state['draft']}\n修改意见：{state['feedback']}"
    
    response = llm.invoke(prompt)
    return {"draft": response.content, "iteration": 1} 


def review_draft(state: AgentState) -> dict:
    print("🧐 [Reviewer] 正在审核文案...")
    prompt = f"""你是一个严格的企业宣发总监。请审核以下文案草稿。
    【企业知识基准】：{state['context']}
    【待审文案】：{state['draft']}
    【要求风格】：{state['tone']}
    
    审核标准：
    1. 文案是否涉及了企业知识基准之外的虚假参数？（幻觉）
    2. 是否符合要求风格？
    
    请务必严格按照以下 JSON 格式输出你的审核结果，不要输出任何额外的解释文字！
    {{
        "is_pass": false,
        "feedback": "如果不合格，给出具体的修改指导。如果完全合格，输出'无'"
    }}"""
    
    response = llm.invoke(prompt)
    
    try:
        clean_text = response.content.replace('```json', '').replace('```', '').strip()
        result = json.loads(clean_text)
        
        return {"is_pass": result.get("is_pass", False), "feedback": result.get("feedback", "格式错误重写")}
        
    except Exception as e:
        print(f"⚠️ JSON 解析失败，原始输出: {response.content}")
        return {"is_pass": False, "feedback": "请严格按照 JSON 格式重新输出审核意见。"}