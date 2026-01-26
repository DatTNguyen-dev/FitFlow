from typing import TypedDict, Annotated, Sequence
import operator
import os
from dotenv import load_dotenv # Thêm dòng này để load .env

# Load API Key từ .env
load_dotenv()

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from utils import get_timetable, update_todo_and_schedule

# --- CẤU HÌNH LLM ---
# Đảm bảo bạn đã có OPENAI_API_KEY trong file .env
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# --- ĐỊNH NGHĨA STATE ---
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next_step: str
    user_schedule: str
    workout_plan: str

# --- ĐỊNH NGHĨA CÁC AGENT NODE ---

# 1. Agent Quản lý Lịch cá nhân (Calendar Manager)
def calendar_agent_node(state):
    action = state.get("next_step")
    
    if action == "FETCH_SCHEDULE":
        # Lấy lịch
        schedule = get_timetable()
        return {
            "messages": [AIMessage(content=f"Đã lấy lịch trình: {schedule}")],
            "user_schedule": schedule
        }
    elif action == "UPDATE_DB":
        # Cập nhật Todo/Timetable
        plan = state.get("workout_plan")
        result = update_todo_and_schedule(plan)
        return {"messages": [AIMessage(content=result)]}
    return {}

# 2. Agent Lên kế hoạch (Planner)
def planner_agent_node(state):
    schedule = state.get("user_schedule")
    # Lấy message đầu tiên từ user (message gốc)
    request = state["messages"][0].content 
    
    prompt = f"""
    Bạn là PT Gym chuyên nghiệp.
    Lịch trình hiện tại của khách: {schedule}
    Yêu cầu của khách: {request}
    
    Hãy tạo một kế hoạch tập luyện ngắn gọn phù hợp với thời gian rảnh trong lịch trình trên.
    Chỉ trả về nội dung kế hoạch.
    """
    response = llm.invoke(prompt)
    return {
        "messages": [response],
        "workout_plan": response.content
    }

# 3. Agent Tổng (Master/Supervisor)
def master_agent_node(state):
    messages = state["messages"]
    last_message = messages[-1]
    
    # Logic điều phối
    # Bắt đầu (User vừa chat) -> Calendar lấy lịch
    if len(messages) == 1 and isinstance(last_message, HumanMessage):
        return {"next_step": "FETCH_SCHEDULE"}
    
    # Đã có lịch -> Gửi cho Planner
    if state.get("user_schedule") and not state.get("workout_plan"):
        return {"next_step": "PLANNING"}
    
    # Đã có Plan -> Gửi Calendar update
    if state.get("workout_plan") and state.get("next_step") == "PLANNING":
        return {"next_step": "UPDATE_DB"}
        
    # Đã update xong -> Kết thúc
    if state.get("next_step") == "UPDATE_DB":
        return {"next_step": "FINISH"}
        
    return {"next_step": "FINISH"}

# --- XÂY DỰNG GRAPH (WORKFLOW) ---
workflow = StateGraph(AgentState)

# Thêm các nodes
workflow.add_node("Master", master_agent_node)
workflow.add_node("CalendarManager", calendar_agent_node)
workflow.add_node("Planner", planner_agent_node)

# Thiết lập điểm bắt đầu
workflow.set_entry_point("Master")

# Thiết lập router (Logic chuyển đổi)
def router(state):
    step = state["next_step"]
    if step == "FETCH_SCHEDULE":
        return "CalendarManager"
    elif step == "PLANNING":
        return "Planner"
    elif step == "UPDATE_DB":
        return "CalendarManager"
    elif step == "FINISH":
        return END
    return END

workflow.add_conditional_edges("Master", router)

# Các agent con sau khi làm xong việc thì quay về Master
workflow.add_edge("CalendarManager", "Master")
workflow.add_edge("Planner", "Master")

# --- QUAN TRỌNG: COMPILE GRAPH ---
# Đây là biến mà app.py đang cố gắng import
app_graph = workflow.compile()