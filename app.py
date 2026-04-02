import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

st.set_page_config(page_title="小红书爆款文案 Agent", page_icon="✍️", layout="centered")

st.title("📕 小红书爆款文案生成 Agent")
st.markdown("基于 LangChain 驱动，快速生成多风格新媒体营销文案。")

with st.sidebar:
    st.header("⚙️ 配置参数")
    api_key = st.text_input("请输入大模型 API Key", type="password")
    st.markdown("[去 DeepSeek 获取免费 API Key](https://platform.deepseek.com/)")
    
    base_url = "https://api.deepseek.com/v1" 
    model_name = "deepseek-chat"
    
    temperature = st.slider("创造力 (Temperature)", min_value=0.0, max_value=1.5, value=0.7)

topic = st.text_input("💡 你想写什么主题？", placeholder="例如：空气炸锅无油炸鸡翅教程")
tone = st.selectbox("🎭 请选择文案风格", ["干货科普风", "闺蜜种草风", "搞笑幽默风", "专业测评风", "情感共鸣风"])

if st.button("🚀 开始生成文案"):
    if not api_key:
        st.error("请先在左侧配置 API Key！")
    elif not topic:
        st.warning("请输入你想写的主题！")
    else:
        with st.spinner("AI 运营专家正在疯狂码字中..."):
            try:
                # 4.1 初始化大模型 (LLM)
                llm = ChatOpenAI(
                    openai_api_key=api_key,
                    openai_api_base=base_url,
                    model_name=model_name,
                    temperature=temperature
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
                response = chain.invoke({"tone": tone, "topic": topic})
                
                st.success("✨ 生成成功！")
                st.markdown("---")
                st.write(response.content)
                
            except Exception as e:
                st.error(f"调用 API 时出现错误：{e}")
