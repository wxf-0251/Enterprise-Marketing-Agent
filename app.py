import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# ==========================================
# 1. 页面基本设置 (UI 部分)
# ==========================================
st.set_page_config(page_title="小红书爆款文案 Agent", page_icon="✍️", layout="centered")

st.title("📕 小红书爆款文案生成 Agent")
st.markdown("基于 LangChain 驱动，快速生成多风格新媒体营销文案。")

# ==========================================
# 2. 侧边栏配置 API 和 参数
# ==========================================
with st.sidebar:
    st.header("⚙️ 配置参数")
    # 让用户输入 API Key，输入时显示为密码格式
    api_key = st.text_input("请输入大模型 API Key", type="password")
    st.markdown("[去 DeepSeek 获取免费 API Key](https://platform.deepseek.com/)")
    
    # 我们这里以 DeepSeek 为例，它的接口完全兼容 OpenAI
    # 如果你用其他平台，只需要改这里的 base_url 和 model_name
    base_url = "https://api.deepseek.com/v1" 
    model_name = "deepseek-chat"
    
    # 创造力参数，值越高生成的文本越发散
    temperature = st.slider("创造力 (Temperature)", min_value=0.0, max_value=1.5, value=0.7)

# ==========================================
# 3. 主界面输入区
# ==========================================
# 用户输入主题和选择风格
topic = st.text_input("💡 你想写什么主题？", placeholder="例如：空气炸锅无油炸鸡翅教程")
tone = st.selectbox("🎭 请选择文案风格", ["干货科普风", "闺蜜种草风", "搞笑幽默风", "专业测评风", "情感共鸣风"])

# ==========================================
# 4. 核心逻辑 (LangChain + Prompt Engineering)
# ==========================================
# 当用户点击“开始生成”按钮时触发
if st.button("🚀 开始生成文案"):
    if not api_key:
        st.error("请先在左侧配置 API Key！")
    elif not topic:
        st.warning("请输入你想写的主题！")
    else:
        # 使用 st.spinner 显示加载动画
        with st.spinner("AI 运营专家正在疯狂码字中..."):
            try:
                # 4.1 初始化大模型 (LLM)
                llm = ChatOpenAI(
                    openai_api_key=api_key,
                    openai_api_base=base_url,
                    model_name=model_name,
                    temperature=temperature
                )
                
                # 4.2 提示词工程 (Prompt Engineering) - 这是这个项目的灵魂！
                # 我们通过系统提示词给 AI 赋予“人设”
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
                
                # 将提示词组合成模板
                prompt_template = ChatPromptTemplate.from_messages([
                    ("system", system_prompt),
                    ("user", user_prompt)
                ])
                
                # 4.3 构建处理链 (Chain)
                # 这使用了 LangChain 的 LCEL 语法：把提示词模板和模型连接起来
                chain = prompt_template | llm
                
                # 4.4 执行调用，传入用户输入的数据
                response = chain.invoke({"tone": tone, "topic": topic})
                
                # 4.5 在页面上展示结果
                st.success("✨ 生成成功！")
                st.markdown("---")
                st.write(response.content)
                
            except Exception as e:
                # 异常处理，防止程序崩溃
                st.error(f"调用 API 时出现错误：{e}")