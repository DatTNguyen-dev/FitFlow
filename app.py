from dotenv import load_dotenv
load_dotenv() 
import os
import streamlit as st
import json
import pandas as pd
from langchain_core.messages import HumanMessage
from agents import app_graph

st.set_page_config(page_title="AI Fitness Hackathon", layout="wide")

# --- LOAD DATA ---
def load_data():
    with open("data.json", "r", encoding='utf-8') as f:
        return json.load(f)

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Fitness Manager")
page = st.sidebar.radio("Chọn trang:", ["Chatbot AI", "Time Table", "To-Do List"])

# --- TRANG 1: CHATBOT ---
if page == "Chatbot AI":
    st.header("🤖 Trợ lý tập luyện AI")
    st.write("Hãy yêu cầu tôi lên lịch tập dựa trên thời gian rảnh của bạn.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ví dụ: Hãy lên lịch tập Cardio cho tôi vào thời gian rảnh hôm nay"):
        # Hiển thị tin nhắn user
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Gọi AI Agent Workflow
        with st.spinner("Các Agent đang thảo luận và lên kế hoạch..."):
            inputs = {"messages": [HumanMessage(content=prompt)]}
            # Chạy graph
            result = app_graph.invoke(inputs)
            
            # Lấy kết quả cuối cùng
            final_plan = result.get("workout_plan", "Xin lỗi, tôi không thể lập kế hoạch.")
            bot_response = f"Đã xong! Tôi đã xem lịch của bạn và thêm kế hoạch sau vào To-Do list:\n\n{final_plan}"

        # Hiển thị tin nhắn bot
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        with st.chat_message("assistant"):
            st.markdown(bot_response)

# --- TRANG 2: TIME TABLE ---
elif page == "Time Table":
    st.header("📅 Lịch trình của bạn")
    data = load_data()
    df = pd.DataFrame(data["timetable"])
    st.table(df)
    
    st.info("Agent 'Quản lý lịch cá nhân' sẽ đọc dữ liệu từ đây để báo cho Planner.")

# --- TRANG 3: TO DO LIST ---
elif page == "To-Do List":
    st.header("✅ Danh sách việc cần làm")
    data = load_data()
    todos = data["todo_list"]
    
    if not todos:
        st.write("Chưa có nhiệm vụ nào.")
    else:
        for i, todo in enumerate(todos):
            cols = st.columns([0.1, 0.9])
            cols[0].checkbox("", key=f"check_{i}")
            cols[1].write(f"**{todo['task']}** ({todo['status']})")
            
    st.success("Khi Agent chốt kế hoạch, task mới sẽ tự động hiện ở đây!")