from .schema import init_db
from .repository import create_user, create_training_plans, add_training_task

init_db()

user = create_user()
plan_id = create_training_plans(user["id"], "2026-02-01", "2026-02-07")

add_training_task(plan_id, "Cardio", 30, "2026-02-01")
add_training_task(plan_id, "Strength", 45, "2026-02-02")

print("DB setup OK")