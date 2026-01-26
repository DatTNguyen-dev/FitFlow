import json
import os

DATA_FILE = "data.json"

# Khởi tạo dữ liệu mẫu nếu chưa có
if not os.path.exists(DATA_FILE):
    default_data = {
        "timetable": [
            {"time": "08:00", "activity": "Học bài"},
            {"time": "12:00", "activity": "Ăn trưa"},
            {"time": "18:00", "activity": "Rảnh rỗi"},
        ],
        "todo_list": []
    }
    with open(DATA_FILE, "w", encoding='utf-8') as f:
        json.dump(default_data, f, ensure_ascii=False, indent=4)

def get_timetable():
    """Lấy lịch trình hiện tại của user."""
    with open(DATA_FILE, "r", encoding='utf-8') as f:
        data = json.load(f)
    return str(data["timetable"])

def update_todo_and_schedule(plan_text):
    """Cập nhật Todo list và Timetable dựa trên kế hoạch."""
    with open(DATA_FILE, "r", encoding='utf-8') as f:
        data = json.load(f)
    
    data["todo_list"].append({"task": f"Thực hiện: {plan_text}", "status": "pending"})
    
    with open(DATA_FILE, "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return "Đã cập nhật To-Do List thành công!"