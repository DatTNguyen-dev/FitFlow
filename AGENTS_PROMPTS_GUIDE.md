# 📝 Agent Prompts System

Hệ thống prompts FitFlow được tổ chức theo role của từng agent. Mỗi agent có một prompt riêng định nghĩa vai trò, chức năng, và cách thức hoạt động.

## 📂 Cấu Trúc Thư Mục

```
fitflowapp/
├── prompts/
│   ├── master_agent_prompt.md          # Master Agent
│   ├── planning_agent_prompt.md        # Planning Agent  
│   ├── schedule_agent_prompt.md        # Schedule Agent
│   └── tracking_agent_prompt.md        # Tracking Agent
└── agents_config/
    ├── agent_manager.py                # Quản lý agents
    └── __init__.py
```

## 🤖 Chi Tiết Từng Agent

### 1️⃣ Master Agent (`master_agent_prompt.md`)
**Vai trò**: Điều phối tất cả các agent khác

**Trách nhiệm**:
- Tiếp nhận và phân tích yêu cầu từ người dùng
- Gọi các agent con phù hợp
- Tổng hợp kết quả
- Đảm bảo quy trình tuân thủ

**Input**: Trình độ, mục tiêu, lịch cá nhân, ràng buộc
**Output**: Kế hoạch hoàn chỉnh, lịch trình, báo cáo

---

### 2️⃣ Planning Agent (`planning_agent_prompt.md`)
**Vai trò**: Thiết kế kế hoạch tập luyện

**Chức năng chính**:
1. Phân tích nhu cầu người dùng
2. Chọn bài tập phù hợp
3. Tạo To-Do list chi tiết
4. Điều chỉnh dựa trên progression

**Tiêu chí theo trình độ**:

| Beginner | Intermediate | Advanced |
|----------|--------------|----------|
| 3-4 days/week | 4-5 days/week | 5-6 days/week |
| Toàn thân/Upper-Lower | PPL Split | Body Part Split |
| 8-12 reps | 6-12 reps | 4-12 reps |

**Output**:
```json
{
  "plan_id": "plan_001",
  "duration_weeks": 12,
  "exercises": [
    {
      "name": "Bench Press",
      "sets": 3,
      "reps": "8-10",
      "weight": "Recommended weight",
      "rest_seconds": 90
    }
  ],
  "progression_plan": "How to progress over time"
}
```

---

### 3️⃣ Schedule Agent (`schedule_agent_prompt.md`)
**Vai trò**: Sắp xếp lịch tập luyện vào khung giờ cá nhân

**Chức năng**:
- Phân tích timetable -> xác định khoảng thời gian rảnh
- Sắp xếp bài tập -> tối ưu năng lượng
- Quản lý phục hồi -> 48 giờ giữa phiên cùng nhóm cơ
- Gửi nhắc nhở -> 1h và 30p trước

**Recovery Strategy**:
- Light days: Cardio nhẹ hoặc yoga
- Rest days: Hoàn toàn nghỉ
- Deload week: Mỗi 4 tuần, giảm 40-50%

**Template Thông Báo**:
```
1 giờ trước: "Trong 1 giờ nữa bạn sẽ bắt đầu tập [workout]. Hãy chuẩn bị!"
30 phút: "Còn 30 phút! [Workout] sắp bắt đầu. Sẵn sàng chưa?"
Bắt đầu: "Đã đến giờ! Bắt đầu [Workout] ngay bây giờ.💪"
Hoàn thành: "Tuyệt vời! Bạn đã hoàn thành [Workout]. Tiếp tục như vậy!"
```

---

### 4️⃣ Tracking Agent (`tracking_agent_prompt.md`)
**Vai trò**: Theo dõi tiến độ và tạo báo cáo đánh giá

**Chỉ số Chính**:

| Loại | Số đo |
|------|-------|
| Sức Mạnh | 1RM, Weight progression, Improvement % |
| Cơ Bắp | Vòng tay/đùi/ngực, Visual assessment |
| Cân Nặng | Weight, Trendline, Changes/week |
| Hiệu Suất | Reps, Time, Recovery intervals |
| Sức Khỏe | Sleep quality, Energy, Soreness, Injury |

**Báo Cáo Template**:

#### Hàng Tuần
```
📊 Báo cáo Tuần [N]

✅ Kết quả:
- Hoàn thành [X]/[Y] bài
- Tổng volume: [Z] kg
- Tuân thủ: [%]

💪 Điểm Mạnh:
- [Strength 1]
- [Strength 2]

⚠️ Cần Cải Thiện:
- [Area 1]
- [Area 2]

📈 Tiến Độ:
- Sức mạnh: [+X%]
- Cân nặng: [+/-X kg]
```

#### Hàng Tháng
```
📅 Báo cáo Tháng [M]

📊 Tổng Quan:
- Tổng buổi: [X]
- Tuân thủ TB: [%]
- Tiến độ chính: [Desc]

🏆 Điểm Nổi Bật:
- [Highlight 1]
- [Highlight 2]

🔧 Cần Điều Chỉnh:
- [Adjustment 1]
```

---

## 🔄 Interaction Flow

```
User Input
    │
    ▼
Master Agent (receives input)
    │
    ├─→ Planning Agent
    │   ├─ Generates exercises
    │   └─ Returns plan
    │
    ├─→ Schedule Agent
    │   ├─ Receives plan
    │   └─ Creates timetable
    │
    ├─→ Tracking Agent
    │   ├─ Reviews metrics
    │   └─ Generates reports
    │
    ▼
Master Agent (aggregates)
    │
    ▼
Output to User
```

---

## 📊 Chỉnh Sửa Prompts

Các file prompt là Markdown được chia thành:

### Structure
```markdown
# Tiêu đề
## Vai trò
Mô tả vai trò của agent

## Chức năng chính
Liệt kê chức năng

## Tiêu chí
Thông số liên quan

## Input
Schema input

## Output
Schema output

## Lưu ý quan trọng
Hướng dẫn đặc biệt
```

### Best Practices

1. **Rõ ràng**: Sử dụng ngôn ngữ chính xác, không mơ hồ
2. **Cấu trúc**: Chia nhỏ thành sections
3. **Ví dụ**: Cung cấp ví dụ JSON
4. **Constraints**: Liệt kê giới hạn rõ ràng
5. **Format**: Định dạng output consistency

---

## 🛠️ Tùy Chỉnh Agents

### Nâng cao tính sáng tạo

```python
# Trong agent_manager.py
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.9,  # Tăng từ 0.7
    max_tokens=4096,  # Tăng từ 2048
)
```

### Thêm Constraints Mới

```markdown
## Ràng buộc Đặc Biệt
- Không đề xuất squat nếu có knee injury
- Hạn chế overhead press nếu shoulder pain
- Bỏ qua dairy nếu lactose intolerant
```

### Custom Goals

```markdown
## Mục tiêu Tùy Chỉnh
- Athletic performance
- Rehabilitation
- Mobility enhancement
- Sports-specific training
```

---

## 📞 Debug Agents

```python
# Shell test
from fitflowapp.agents_config import agent_manager

# Test Planning Agent
response = agent_manager.process_request(
    {'current_level': 'beginner', 'goal': 'weight_loss'},
    agent_type='planning'
)

print(response)
```

---

## 📌 Prompt Best Practices

✅ **DO**:
- Stack multiple constraints for better output
- Use structured JSON for input/output
- Provide examples
- Be specific about role and responsibility

❌ **DON'T**:
- Overly complex prompts
- Mix multiple roles in one agent
- Forget to define failures/edge cases
- Use ambiguous terminology

---

## 🎯 Examples

### Example 1: Customizing Planning Agent

Edit `planning_agent_prompt.md`:

```markdown
## Thêm Support cho Home Workout

### Home Workout Modifications
- Dumbbells max 40kg
- Bodyweight exercises prioritized
- No expensive equipment required
```

### Example 2: Adding New Report Type

Edit `tracking_agent_prompt.md`:

```markdown
## Thêm Quarterly Report

### Quarterly Report (3 months)
- Major milestones
- Long-term trends
- Comparison with previous quarters
- Year-goal projection
```

---

**Last Updated**: February 5, 2026
**Model**: Gemini 2.5 Flash
**Status**: Production Ready ✅
