# FitFlow - Personalized Workout Scheduling System

## 📋 Tổng Quan

FitFlow là một ứng dụng web thông minh dành cho việc xây dựng lịch trình tập luyện cá nhân hóa. Hệ thống sử dụng các AI Agents (dựa trên LangChain và Gemini 2.5 Flash) để:

- 📝 **Lên To-Do List**: Tạo danh sách công việc chi tiết cho mỗi phiên tập luyện
- 📅 **Soạn Timetable phù hợp**: Sắp xếp lịch tập luyện theo thời gian cá nhân
- 📊 **Track Tiến Trình**: Theo dõi hiệu suất và tiến độ tập luyện
- 🎯 **Đánh Giá Tiến Độ**: Tạo báo cáo chi tiết về các điểm cần cải thiện
- 🔔 **Nhắc Nhở Luyện Tập**: Gửi thông báo và nhắc nhở kịp thời

---

## 🏗️ Kiến Trúc Hệ Thống

### Backend Stack
- **Framework**: Django 6.0.1
- **REST API**: Django REST Framework
- **AI/ML**: LangChain + Gemini 2.5 Flash
- **Database**: SQLite (có thể mở rộng sang PostgreSQL)
- **Task Queue**: Celery + Redis (cho scheduled notifications)

### Frontend Stack
- **Framework**: React + Vite
- **Styling**: CSS + Tailwind CSS
- **HTTP Client**: Axios/Fetch API

---

## 🤖 Agents Overview

### 1. **Master Agent** (Điều phối viên)
- **Vai trò**: Điều phối các agent khác
- **Chức năng**:
  - Nhận yêu cầu từ người dùng
  - Phân phối cho agent thích hợp
  - Tổng hợp kết quả đầu ra

### 2. **Planning Agent** (Agent Lên Kế Hoạch)
- **Vai trò**: Thiết kế kế hoạch tập luyện
- **Input**: 
  - Trình độ hiện tại (beginner, intermediate, advanced)
  - Mục tiêu fitness (weight loss, muscle gain, endurance, flexibility)
  - Thời gian có sẵn
  - Ràng buộc (chấn thương, dị ứng)
- **Output**:
  - Danh sách bài tập chi tiết
  - Sets, reps, weight recommendations
  - To-Do list cho mỗi phiên
  - Lịch trình luyện tập theo tuần

### 3. **Schedule Management Agent** (Agent Quản Lý Lịch)
- **Vai trò**: Sắp xếp lịch tập luyện
- **Chức năng**:
  - Phân tích timetable cá nhân
  - Sắp xếp các bài tập vào khung giờ thích hợp
  - Quản lý ngày phục hồi (recovery days)
  - Tạo hệ thống nhắc nhở
- **Output**:
  - Lịch trình chi tiết theo ngày/giờ
  - Hệ thống notification
  - Kế hoạch phục hồi

### 4. **Progress Tracking & Performance Agent** (Agent Theo Dõi Tiến Độ)
- **Vai trò**: Giám sát hiệu suất
- **Chức năng**:
  - Thu thập dữ liệu tập luyện
  - Phân tích tiến độ
  - Tạo báo cáo đánh giá
  - Đề xuất cải thiện
- **Output**:
  - Báo cáo hàng tuần/tháng
  - Phân tích điểm mạnh/yếu
  - Đề xuất điều chỉnh kế hoạch

---

## 📁 Cấu Trúc Dữ Liệu

### Models chính:

```
UserProfile
├── BasicInfo (age, weight, height, level)
├── FitnessGoal
│   └── primary_goal, hours_per_week, target_date
├── PersonalSchedule
│   └── availability (day, start_time, end_time)
├── ConstraintAndPreference
│   └── injuries, allergies, preferred_exercises, equipment
├── ExercisePlan
│   └── plan_data (JSON từ Planning Agent)
├── WorkoutSchedule
│   └── schedule_data (JSON từ Schedule Agent)
├── WorkoutSession
│   ├── scheduled_date, scheduled_time, status
│   └── exercises (JSON)
├── ExerciseLog
│   └── Chi tiết từng bài tập
├── BodyMetrics
│   ├── weight, body_fat, measurements
│   └── subjective_data (sleep, energy, soreness)
├── ProgressReport
│   ├── report_type (weekly, monthly)
│   └── recommendations (JSON)
└── Notification
    └── Thông báo nhắc nhở
```

---

## 🚀 Cài Đặt và Khởi Chạy

### 1. Yêu Cầu Hệ Thống
- Python 3.9+
- Node.js 18+
- pip, npm

### 2. Cài Đặt Backend

```bash
# Tạo virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows
source venv/bin/activate  # macOS/Linux

# Cài đặt dependencies
pip install -r requirements.txt

# Tạo .env file
echo "GOOGLE_API_KEY=your_gemini_api_key_here" > .env

# Chạy migrations
python manage.py makemigrations
python manage.py migrate

# Tạo superuser
python manage.py createsuperuser

# Khởi chạy server
python manage.py runserver
```

### 3. Cài Đặt Frontend

```bash
cd frontend

# Cài dependencies
npm install

# Khởi chạy dev server
npm run dev
```

### 4. Thiết Lập Google Gemini API

1. Truy cập [Google AI Studio](https://aistudio.google.com)
2. Tạo API Key
3. Thêm vào file `.env`

```env
GOOGLE_API_KEY=your_api_key_here
```

---

## 📚 API Endpoints

### User Profile
```
GET    /api/profiles/              # Lấy hồ sơ người dùng
POST   /api/profiles/              # Tạo hồ sơ
PUT    /api/profiles/{id}/         # Cập nhật hồ sơ
```

### Fitness Goals
```
GET    /api/goals/                 # Lấy mục tiêu
POST   /api/goals/                 # Tạo mục tiêu
```

### Personal Schedule
```
GET    /api/schedules/personal/    # Lấy lịch cá nhân
POST   /api/schedules/personal/    # Thêm khung giờ rảnh
```

### Exercise Plans
```
GET    /api/plans/exercise/        # Lấy kế hoạch
POST   /api/plans/exercise/generate_plan/  # Tạo kế hoạch mới
```

### Workout Schedules
```
GET    /api/schedules/workout/     # Lấy lịch tập
POST   /api/schedules/workout/generate_schedule/  # Tạo lịch
```

### Workout Sessions
```
GET    /api/sessions/              # Lấy phiên tập
GET    /api/sessions/upcoming/     # Sắp tới
GET    /api/sessions/history/      # Lịch sử
POST   /api/sessions/              # Tạo phiên
```

### Body Metrics
```
GET    /api/metrics/               # Lấy chỉ số cơ thể
POST   /api/metrics/               # Thêm đo lường
```

### Progress Reports
```
GET    /api/reports/               # Lấy báo cáo
POST   /api/reports/generate_report/  # Tạo báo cáo mới
```

### Notifications
```
GET    /api/notifications/         # Lấy thông báo
GET    /api/notifications/unread/  # Chưa đọc
POST   /api/notifications/mark_all_as_read/  # Đánh dấu đã đọc
```

---

## 🔧 Cấu Hình Agents

Các prompt cho agents được lưu trong thư mục `fitflowapp/prompts/`:

- `master_agent_prompt.md` - Prompt cho Master Agent
- `planning_agent_prompt.md` - Prompt cho Planning Agent
- `schedule_agent_prompt.md` - Prompt cho Schedule Agent
- `tracking_agent_prompt.md` - Prompt cho Tracking Agent

### Chỉnh Sửa Prompts

Mỗi prompt được viết bằng Markdown và chứa:
1. Vai trò (Role)
2. Chức năng chính (Main Functions)
3. Tiêu chí thiết kế (Design Criteria)
4. Input/Output format (JSON schema)

Bạn có thể chỉnh sửa trực tiếp các file này để thay đổi behavior của agents.

---

## 💡 Ví Dụ Sử Dụng

### Tạo Kế Hoạch Tập Luyện

```python
from fitflowapp.agents_config import agent_manager

user_input = {
    'current_level': 'beginner',
    'goal': 'muscle_gain',
    'hours_per_week': 4,
    'age': 25,
    'weight_kg': 70,
    'height_cm': 180,
    'injuries': [],
    'preferred_exercises': ['bench press', 'squats', 'deadlifts']
}

response = agent_manager.process_request(user_input, agent_type='planning')
print(response)
```

### Tạo Lịch Tập Luyện

```python
schedule_input = {
    'exercise_plan': response,
    'personal_timetable': {
        'Monday': {'start_time': '09:00', 'end_time': '11:00'},
        'Wednesday': {'start_time': '14:00', 'end_time': '16:00'},
        'Friday': {'start_time': '18:00', 'end_time': '20:00'},
    },
    'preferences': {
        'preferred_times': ['morning', 'evening'],
        'location': 'gym'
    }
}

schedule = agent_manager.process_request(schedule_input, agent_type='schedule')
print(schedule)
```

### Theo Dõi Tiến Độ

```python
tracking_input = {
    'user_id': 1,
    'report_type': 'weekly',
    'workouts_completed': 3,
    'workouts_planned': 4,
    'adherence_rate': 75,
    'metrics': {
        'weight_change': -1.5,  # kg
        'strength_improvement': 5,  # %
    }
}

report = agent_manager.process_request(tracking_input, agent_type='tracking')
print(report)
```

---

## 📊 Luồng Công Việc

```
┌─────────────────────────┐
│   User Input            │
│ (Level, Goal, Schedule) │
└────────────┬────────────┘
             │
      ┌──────▼──────┐
      │Master Agent │
      └──────┬──────┘
             │
      ┌──────┴──────┬──────────┬──────────┐
      │             │          │          │
      ▼             ▼          ▼          ▼
 ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐
 │Planning│  │Schedule│  │Tracking│  │Master  │
 │Agent   │  │Agent   │  │Agent   │  │Agent   │
 └────────┘  └────────┘  └────────┘  └────────┘
      │             │          │          │
      └──────┬──────┴──────────┴──────────┘
             │
      ┌──────▼──────┐
      │  Output     │
      │ - Plan      │
      │ - Schedule  │
      │ - Reports   │
      │ - Reminders │
      └─────────────┘
```

---

## 📝 Ghi Chú Quan Trọng

### Gemini 2.5 Flash Model
- **Temperature**: 0.7 (cân bằng giữa sáng tạo và tính nhất quán)
- **Max Tokens**: 2048
- **Model**: `gemini-2.5-flash` (nhanh, chi phí thấp, đủ mạnh)

### Database
- Sử dụng SQLite cho development
- Cần chuyển sang PostgreSQL cho production
- Tất cả dữ liệu quan trọng được lưu dưới dạng JSON để linh hoạt

### Performance
- Lưu cache kết quả từ agents
- Sử dụng Celery để xử lý background tasks
- Redis cho caching và message queue

---

## 🐛 Troubleshooting

### ImportError: No module named 'langchain'
```bash
pip install langchain==0.1.0 langchain-google-genai==0.0.10
```

### GOOGLE_API_KEY not set
```bash
# Tạo file .env
echo "GOOGLE_API_KEY=your_key" > .env
```

### Migrations error
```bash
python manage.py makemigrations --empty fitflowapp --name initial
python manage.py migrate
```

---

## 📞 Support

Để có thêm thông tin, vui lòng liên hệ hoặc tạo issue trong repository.

---

## 📄 License

MIT License - Xem file LICENSE để chi tiết
