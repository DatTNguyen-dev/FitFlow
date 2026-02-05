# 🚀 Quick Start Guide - FitFlow

## ⚡ Bắt Đầu Nhanh (5 phút)

### Step 1: Chuẩn bị môi trường

```bash
# Mở Terminal/PowerShell tại thư mục d:\FitFlow

# Tạo virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Cài dependencies
pip install -r requirements.txt
```

### Step 2: Cấu hình Gemini API

```bash
# Lấy API Key từ https://aistudio.google.com
# Tạo file .env
echo GOOGLE_API_KEY=paste_your_key_here > .env
```

### Step 3: Setup Database

```bash
# Tạo migrations
python manage.py makemigrations

# Chạy migrations
python manage.py migrate

# Tạo superuser (admin account)
python manage.py createsuperuser
# Username: admin
# Password: (tự chọn)
```

### Step 4: Khởi chạy Backend

```bash
python manage.py runserver
# Server chạy tại http://localhost:8000
```

### Step 5: Frontend Setup

```bash
# Terminal mới, chạy từ folder project root
cd frontend
npm install
npm run dev
# Frontend chạy tại http://localhost:5173
```

---

## 📋 Checklist Thiết Lập

- [ ] Virtual environment được kích hoạt
- [ ] requirements.txt được cài đặt
- [ ] GOOGLE_API_KEY được thiết lập trong .env
- [ ] Database migrations hoàn tất
- [ ] Backend server chạy ở port 8000
- [ ] Frontend dev server chạy ở port 5173
- [ ] Có thể truy cập http://localhost:5173

---

## 🧪 Test API dùng cURL

### Test 1: Tạo kế hoạch tập luyện

```bash
curl -X POST http://localhost:8000/api/plans/exercise/generate_plan/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_token_here" \
  -d '{
    "current_level": "beginner",
    "goal": "muscle_gain",
    "hours_per_week": 4
  }'
```

### Test 2: Lấy thông báo

```bash
curl http://localhost:8000/api/notifications/unread/ \
  -H "Authorization: Bearer your_token_here"
```

---

## 🔑 Key Files

| File | Mô tả |
|------|-------|
| `fitflowapp/agents.py` | Main agents module |
| `fitflowapp/agents_config/agent_manager.py` | Agent initialization & management |
| `fitflowapp/prompts/` | Prompt files cho từng agent |
| `fitflowapp/models.py` | Django models |
| `fitflowapp/views.py` | API views/endpoints |
| `fitflowapp/api/urls.py` | URL routing |
| `fitflow/settings.py` | Django settings |

---

## 🎯 Agents Architecture

```
Master Agent (Coordinator)
│
├─→ Planning Agent: Tạo kế hoạch tập
│   ├─ Input: Level, Goal, Time
│   └─ Output: Exercises, Sets, Reps
│
├─→ Schedule Agent: Sắp xếp lịch
│   ├─ Input: Plan, Personal Schedule
│   └─ Output: Weekly Timetable, Notifications
│
└─→ Tracking Agent: Track tiến độ
    ├─ Input: Performance Metrics
    └─ Output: Reports, Recommendations
```

---

## 📱 API Response Example

### Tạo Exercise Plan

**Request:**
```json
{
  "current_level": "beginner",
  "goal": "weight_loss",
  "hours_per_week": 3
}
```

**Response:**
```json
{
  "success": true,
  "agent": "Planning Agent",
  "response": "Detailed plan with exercises...",
  "data": {
    "plan_id": "plan_001",
    "exercises": [
      {
        "name": "Bench Press",
        "sets": 3,
        "reps": "8-10",
        "weight": "60kg"
      }
    ]
  }
}
```

---

## 🔐 Environment Variables

```env
# .env file
GOOGLE_API_KEY=your_gemini_api_key
DEBUG=True
SECRET_KEY=your_django_secret_key
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## ❓ FAQ

**Q: Cần API Key từ đâu?**
A: https://aistudio.google.com

**Q: Port 8000 đang bị chiếm?**
A: `python manage.py runserver 8001`

**Q: Làm sao reset database?**
A: Delete `db.sqlite3` rồi chạy `python manage.py migrate` lại

**Q: Migrations không chạy?**
A: Xóa folder `fitflowapp/migrations/` (giữ `__init__.py`), rồi `makemigrations`

---

## 📞 Debugging Tips

```bash
# Xem database
python manage.py shell
>>> from fitflowapp.models import UserProfile
>>> UserProfile.objects.all()

# Xem logs chi tiết
DEBUG = True  # trong settings.py

# Test Agent
python manage.py shell
>>> from fitflowapp.agents_config import agent_manager
>>> agent_manager.process_request({'test': 'data'}, 'master')
```

---

## ✅ Tiếp Theo

1. Tạo user account
2. Setup hồ sơ fitness
3. Nhập mục tiêu và schedule cá nhân
4. Generate kế hoạch tập luyện
5. Theo dõi tiến độ

Happy Training! 💪
