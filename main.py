import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv


load_dotenv()


API_KEY = os.getenv("DEEPSEEK_API_KEY")

if not API_KEY:
    
    raise ValueError("未找到 DEEPSEEK_API_KEY，请检查 .env 文件是否配置正确！")

app = FastAPI(title="小红书文案生成 API", description="企业级安全配置示范")


class CopyRequest(BaseModel):
    topic: str
    tone: str
    temperature: float = 0.7 

@app.post("/api/generate_copy")
def generate_copy(request: CopyRequest):
    base_url = "https://api.deepseek.com/v1" 
    model_name = "deepseek-chat"
    
    try:

        llm = ChatOpenAI(
            openai_api_key=API_KEY, 
            openai_api_base=base_url,
            model_name=model_name,
            temperature=request.temperature
        )
        
        system_prompt = """你是一个拥有百万粉丝的小红书爆款运营专家。
        你深谙小红书平台的流量密码，精通引发用户共鸣、使用恰当的Emoji表情，以及设置悬念和互动引导。
        你的任务是根据用户给定的主题和风格，输出一篇高质量的小红书文案。"""
        
        user_prompt = """请以【{tone}】写一篇关于【{topic}】的小红书文案。
        必须包含以下结构：
        1. 吸引眼球的标题（给出3个供选择）
        2. 痛点引入（抓住读者眼球）
        3. 正文干货（条理清晰，多用动词）
        4. 金句总结
        5. 互动引导（求赞、收藏、评论）
        请合理排布段落和Emoji表情，使其符合小红书的阅读习惯。"""
        
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", user_prompt)
        ])
        
        chain = prompt_template | llm
        
        response = chain.invoke({"tone": request.tone, "topic": request.topic})
        
        return {
            "code": 200,
            "message": "success",
            "data": {
                "content": response.content
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"调用大模型 API 时出现错误：{str(e)}")