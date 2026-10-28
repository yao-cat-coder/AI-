import streamlit as st
import json
import os
from openai import OpenAI
st.set_page_config(page_title = "任务管家", page_icon = "🤵", layout = "wide")
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #FDF8F5 !important;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
p, span, label, h1, h2, h3, h4, div {
    color: #4A4A4A !important;
    font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
}
.stTextInput>div>div>input {
    background-color: #FFFFFF !important;
    color: #333333 !important;
    border: 2px solid #EAEAEA !important;
    border-radius: 12px !important;
    padding: 10px 15px !important;
    transition: all 0.3s ease;
}
.stTextInput>div>div>input:focus {
    border-color: #FF8C61 !important;
    box-shadow: 0 0 8px rgba(255, 140, 97, 0.2) !important;
}
.stButton>button {
    background: #FF8C61 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 20px !important;
    padding: 10px 24px !important;
    font-weight: bold !important;
    box-shadow: 0 4px 12px rgba(255, 140, 97, 0.3) !important;
    transition: all 0.2s ease !important;
}
.stButton>button:hover {
    background: #FF7A45 !important;
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(255, 140, 97, 0.4) !important;
}
.task-card {
    background-color: #FFFFFF;
    border-radius: 15px;
    padding: 16px 20px;
    margin-bottom: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
    border-left: 6px solid #FF8C61;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.task-name {
    font-size: 16px;
    font-weight: bold;
    color: #333333 !important;
}
.task-time {
    font-size: 14px;
    color: #999999 !important;
    background: #FDF8F5;
    padding: 4px 10px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)
st.title("欢迎来到智慧管家系统")
st.write("请输入大白话，如“明天早上七点要上早八”")
def save_tasks(task_name, task_time):
    file_path = "my_task.json"
    tasks = []
    new_task = {"task": task_name, "time":task_time}
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8")as f:
            tasks = json.load(f)
    tasks.append(new_task)
    with open(file_path, "w", encoding="utf-8")as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)
client = OpenAI(
    api_key = "54062a9348f54864a5628daf55b6f76e.WAEKFAsmcFaeAnBX",
    base_url = "https://open.bigmodel.cn/api/paas/v4/"
)
user_input = st.text_input("你想记录点什么", placeholder = "例如这周末要把思政作业交了")
col1, col2 = st.columns(2)
with col1:
    if st.button("让AI提取并记录", use_container_width = True):
        if user_input:
            prompft = f"""
            你作为任务管家，从用户的输入中提取信息严格用JSON格式来回答：
            {{"task":"任务名", "time":"时间"}}绝对不可以自己另外添加文字或字符！
            {user_input}
            """
            response = client.chat.completions.create(
                model = "glm-4-flash",
                messages = [{"role":"user", "content": prompft}]
            )
            ai_reply = response.choices[0].message.content
            try:
                clean_reply = ai_reply.replace("```json", "").replace("```", "")
                clean_data = json.loads(clean_reply)
                save_tasks(clean_data["task"], clean_data["time"])
                st.success("收录成功！")
                st.rerun()
            except Exception as e:
                st.error(f"输入失败，原因是{e}")
        else:
            st.warning("请先输入内容哦~")
with col2:
    if st.button("一键清空", use_container_width=True):
        with open("my_task.json", "w", encoding="utf-8")as f:
            json.dump([], f)
        st.rerun()
st.divider()
st.subheader("任务展示区")
if os.path.exists("my_task.json"):
    with open("my_task.json", "r", encoding="utf-8")as f:
        tasks = json.load(f)
    if not tasks:
        st.info("目前没有任务哦~")
    else:
        for i,t in enumerate(tasks,1):
            st.write(f"{i}. **{t['task']}**(时间：{t['time']})")
else:
    st.info("目前没有任务哦~")

