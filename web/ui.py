import streamlit as st
import requests

st.title("📕 企业级闭环营销 Agent (PoC)")

topic = st.text_input("💡 你想写什么主题？")
tone = st.selectbox("🎭 请选择文案风格", ["干货科普风", "闺蜜种草风"])

if st.button("🚀 开始生成文案"):
    with st.spinner("Agent 工作流已启动 (正在进行 检索->生成->审核 闭环)..."):
        try: 
            response = requests.post(
                "http://localhost:8000/api/generate_copy",
                json={"topic": topic, "tone": tone}
            )
            
            if response.status_code == 200:
                result = response.json()
                data = result.get('data', {})
                
                content = data.get('content', '文案生成完毕。')
                iterations = data.get('iterations_run', '多')
                
                st.success(f"✨ 生成成功！(Agent 内部进行了 {iterations} 轮自我反思与重写)")
                st.markdown("---")
                st.markdown(content)
            else:
                st.error(f"服务端错误详情: {response.json().get('detail', response.text)}")
                
        except Exception as e: 
            st.error(f"网络请求失败：{e}")