import streamlit as st
import json
import os
from openai import OpenAI
st.set_page_config(page_title = "任务管家", page_icon = "🤵", layout = "wide")
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

