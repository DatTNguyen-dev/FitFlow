# FitFlow - Complete Usage Examples

This file contains complete working examples of how to use the FitFlow system.

## Example 1: Generate Exercise Plan via API

### HTTP Request

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

### Python Request

```python
import requests
import json

BASE_URL = "http://localhost:8000/api"
TOKEN = "your_auth_token"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Create user profile first
profile_data = {
    "current_level": "beginner",
    "age": 25,
    "weight_kg": 70,
    "height_cm": 180
}

response = requests.post(
    f"{BASE_URL}/profiles/",
    json=profile_data,
    headers=headers
)
print(response.json())

# Generate exercise plan
response = requests.post(
    f"{BASE_URL}/plans/exercise/generate_plan/",
    headers=headers
)
print("Plan generated:")
print(json.dumps(response.json(), indent=2))
```

## Example 2: Generate Workout Schedule

```python
import requests

BASE_URL = "http://localhost:8000/api"
TOKEN = "your_auth_token"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Add personal schedule (when you're available)
schedule_data = {
    "day": "Monday",
    "start_time": "09:00",
    "end_time": "11:00",
    "available": True
}

requests.post(
    f"{BASE_URL}/schedules/personal/",
    json=schedule_data,
    headers=headers
)

# Repeat for other days...

# Generate workout schedule
response = requests.post(
    f"{BASE_URL}/schedules/workout/generate_schedule/",
    json={"preferred_times": ["morning", "evening"]},
    headers=headers
)

schedule = response.json()
print("Workout schedule generated:")
for day, workout in schedule.get('weekly_timetable', {}).items():
    print(f"{day}: {workout['time']}")
```

## Example 3: Log a Workout Session

```python
import requests
from datetime import date

BASE_URL = "http://localhost:8000/api"
TOKEN = "your_auth_token"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Create a completed workout session
session_data = {
    "scheduled_date": str(date.today()),
    "scheduled_time": "09:00",
    "status": "completed",
    "exercises": [
        {
            "name": "Bench Press",
            "sets": 3,
            "reps": "10",
            "weight": 60
        },
        {
            "name": "Incline Dumbbell Press",
            "sets": 3,
            "reps": "10",
            "weight": 30
        }
    ],
    "duration_minutes": 60,
    "notes": "Great workout, felt strong"
}

response = requests.post(
    f"{BASE_URL}/sessions/",
    json=session_data,
    headers=headers
)

session = response.json()
print(f"Session created: {session['id']}")

# Log detailed exercise data
exercise_log = {
    "exercise_name": "Bench Press",
    "planned_sets": 3,
    "planned_reps": "10",
    "planned_weight_kg": 60,
    "actual_sets": 3,
    "actual_reps": "10",
    "actual_weight_kg": 60,
    "rpe": 8,  # Rate of Perceived Exertion 1-10
    "completed": True,
    "notes": "Perfect form"
}

# Note: Exercise logs would typically be created through a nested endpoint
```

## Example 4: Log Body Metrics

```python
import requests
from datetime import date

BASE_URL = "http://localhost:8000/api"
TOKEN = "your_auth_token"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

metrics = {
    "weight_kg": 68.5,
    "body_fat_percentage": 15.5,
    "chest_cm": 95,
    "arm_cm": 33,
    "waist_cm": 82,
    "thigh_cm": 55,
    "sleep_quality": 8,
    "energy_level": 7,
    "muscle_soreness": 4,
    "injury_status": "none"
}

response = requests.post(
    f"{BASE_URL}/metrics/",
    json=metrics,
    headers=headers
)

print("Metrics logged:", response.json())
```

## Example 5: Generate Progress Report

```python
import requests
import json

BASE_URL = "http://localhost:8000/api"
TOKEN = "your_auth_token"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Generate weekly report
response = requests.post(
    f"{BASE_URL}/reports/generate_report/",
    json={"report_type": "weekly"},
    headers=headers
)

report = response.json()
print("Weekly Report Generated:")
print(f"Adherence Rate: {report['adherence_rate']}%")
print(f"Summary:\n{report['summary']}")

# Generate monthly report
response = requests.post(
    f"{BASE_URL}/reports/generate_report/",
    json={"report_type": "monthly"},
    headers=headers
)

print("\nMonthly Report Generated")
```

## Example 6: Get Upcoming Workouts

```python
import requests

BASE_URL = "http://localhost:8000/api"
TOKEN = "your_auth_token"

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

# Get upcoming workouts
response = requests.get(
    f"{BASE_URL}/sessions/upcoming/",
    headers=headers
)

workouts = response.json()
print("Upcoming Workouts:")
for workout in workouts:
    print(f"- {workout['scheduled_date']} @ {workout['scheduled_time']}")
```

## Example 7: Using Agents Directly (Backend)

```python
from fitflowapp.agents_config.agent_manager import agent_manager
from fitflowapp.models import UserProfile

# Get user
user_profile = UserProfile.objects.get(user__username='john')

# Create input for Planning Agent
input_data = {
    'user_id': user_profile.id,
    'current_level': user_profile.current_level,
    'goal': user_profile.fitness_goal.primary_goal,
    'age': user_profile.age,
    'weight_kg': user_profile.weight_kg,
    'height_cm': user_profile.height_cm,
    'hours_per_week': user_profile.fitness_goal.hours_per_week,
}

# Get response from Planning Agent
response = agent_manager.process_request(input_data, agent_type='planning')

print("Agent Response:")
print(response['response'])

if 'data' in response:
    print("\nStructured Data:")
    import json
    print(json.dumps(response['data'], indent=2))
```

## Example 8: Enable Notifications

```python
import requests
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/api"
TOKEN = "your_auth_token"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Create notification for upcoming workout
tomorrow = datetime.now() + timedelta(days=1)
notification = {
    "notification_type": "reminder",
    "title": "Workout Reminder",
    "message": "Don't forget your workout tomorrow at 09:00!",
    "scheduled_time": tomorrow.isoformat()
}

response = requests.post(
    f"{BASE_URL}/notifications/",
    json=notification,
    headers=headers
)

print("Notification created:", response.json()['id'])

# Get unread notifications
response = requests.get(
    f"{BASE_URL}/notifications/unread/",
    headers=headers
)

notifications = response.json()
print(f"Unread notifications: {len(notifications)}")
for notif in notifications:
    print(f"- {notif['title']}: {notif['message']}")

# Mark all as read
requests.post(
    f"{BASE_URL}/notifications/mark_all_as_read/",
    headers=headers
)
```

## Example 9: Complete Workflow

```python
import requests
from datetime import date

BASE_URL = "http://localhost:8000/api"
TOKEN = "your_auth_token"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

print("=== FitFlow Complete Workflow ===\n")

# Step 1: Create User Profile
print("1. Creating user profile...")
profile = {
    "current_level": "beginner",
    "age": 28,
    "weight_kg": 75,
    "height_cm": 180
}
profile_resp = requests.post(f"{BASE_URL}/profiles/", json=profile, headers=headers)
profile_id = profile_resp.json()['id']
print(f"✓ Profile created: {profile_id}\n")

# Step 2: Set Fitness Goal
print("2. Setting fitness goal...")
goal = {
    "primary_goal": "muscle_gain",
    "hours_per_week": 4,
    "target_weight_kg": 85,
    "target_date": "2026-08-05"
}
goal_resp = requests.post(f"{BASE_URL}/goals/", json=goal, headers=headers)
print(f"✓ Goal set: Muscle gain, {goal['hours_per_week']} hours/week\n")

# Step 3: Add Personal Schedule
print("3. Adding personal schedule...")
schedule = {
    "day": "Monday",
    "start_time": "09:00",
    "end_time": "11:00"
}
requests.post(f"{BASE_URL}/schedules/personal/", json=schedule, headers=headers)
print("✓ Schedule added: Monday 09:00-11:00\n")

# Step 4: Generate Exercise Plan
print("4. Generating exercise plan...")
plan_resp = requests.post(f"{BASE_URL}/plans/exercise/generate_plan/", headers=headers)
print("✓ Plan generated\n")

# Step 5: Generate Workout Schedule
print("5. Generating workout schedule...")
schedule_resp = requests.post(f"{BASE_URL}/schedules/workout/generate_schedule/", headers=headers)
print("✓ Workout schedule created\n")

# Step 6: Log Workout Session
print("6. Logging workout session...")
session = {
    "scheduled_date": str(date.today()),
    "scheduled_time": "09:00",
    "status": "completed",
    "duration_minutes": 60,
    "exercises": [
        {"name": "Bench Press", "sets": 3, "reps": "10", "weight": 60}
    ]
}
session_resp = requests.post(f"{BASE_URL}/sessions/", json=session, headers=headers)
print("✓ Workout session logged\n")

# Step 7: Log Body Metrics
print("7. Logging body metrics...")
metrics = {
    "weight_kg": 74.5,
    "body_fat_percentage": 18,
    "sleep_quality": 8,
    "energy_level": 7
}
requests.post(f"{BASE_URL}/metrics/", json=metrics, headers=headers)
print("✓ Metrics logged\n")

# Step 8: Generate Progress Report
print("8. Generating progress report...")
report_resp = requests.post(f"{BASE_URL}/reports/generate_report/", 
                            json={"report_type": "weekly"}, headers=headers)
print("✓ Progress report generated\n")

# Step 9: Get Upcoming Workouts
print("9. Getting upcoming workouts...")
upcoming_resp = requests.get(f"{BASE_URL}/sessions/upcoming/", headers=headers)
upcoming = upcoming_resp.json()
print(f"✓ {len(upcoming)} upcoming workouts\n")

print("=== Workflow Complete ===")
```

## Example 10: Django Shell Usage

```python
# Run: python manage.py shell

from fitflowapp.models import *
from fitflowapp.agents_config import agent_manager
from django.contrib.auth.models import User
import json

# Create a test user
user = User.objects.create_user('testuser', 'test@example.com', 'password123')

# Create profile
profile = UserProfile.objects.create(
    user=user,
    current_level='beginner',
    age=25,
    weight_kg=70,
    height_cm=180
)

# Create fitness goal
goal = FitnessGoal.objects.create(
    user_profile=profile,
    primary_goal='weight_loss',
    hours_per_week=4,
    target_date='2026-06-05'
)

# Test the Planning Agent
input_data = {
    'current_level': 'beginner',
    'goal': 'weight_loss',
    'age': 25,
    'weight_kg': 70,
    'height_cm': 180,
    'hours_per_week': 4
}

response = agent_manager.process_request(input_data, agent_type='planning')
print("Planning Agent Response:")
print(json.dumps(response, indent=2))

# View all user profiles
profiles = UserProfile.objects.all()
for p in profiles:
    print(f"{p.user.username} - {p.current_level}")
```

---

## Key API Response Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Server Error |

## Common Error Responses

```json
{
  "error": "GOOGLE_API_KEY not configured"
}
```

```json
{
  "error": "User profile not found"
}
```

```json
{
  "error": "Insufficient data provided"
}
```

---

For more information, see:
- FITFLOW_DOCUMENTATION.md
- QUICKSTART.md
- AGENTS_PROMPTS_GUIDE.md
- CONFIG_GUIDE.md
