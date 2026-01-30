import uuid
from datetime import datetime
from .connection import get_connection

def create_user():
    conn = get_connection()
    cursor = conn.cursor()

    user_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat()

    cursor.execute(
        "INSERT INTO users (id, created_at) VALUES (?, ?)",
        (user_id, created_at)
    )

    conn.commit()
    conn.close()

    return {
        "id": user_id,
        "created_at": created_at
    }

def create_training_plans(user_id, start_date, end_date):
    conn = get_connection()
    cursor = conn.cursor()

    plan_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat()

    cursor.execute(
        """
        INSERT INTO training_plans (id, user_id, start_date, end_date, created_at)
        VALUES(?, ?, ?, ?, ?)
        """,
        (plan_id, user_id, start_date, end_date, created_at)
    )

    conn.commit()
    conn.close()

    return plan_id

def add_training_task(plan_id, name, duration_minutes, scheduled_date):
    conn = get_connection()
    cursor = conn.cursor()

    task_id = str(uuid.uuid4())

    cursor.execute(
        """
        INSERT INTO training_tasks (id, plan_id, name, duration_minutes, scheduled_date)
        VALUES (?, ?, ?, ?, ?)
        """,
        (task_id, plan_id, name, duration_minutes, scheduled_date)
    )

    conn.commit()
    conn.close()

    return task_id

def get_user_plans(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM training_plans WHERE user_id = ?",
        (user_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]

def get_plan_tasks(plan_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM training_tasks WHERE plan_id = ?",
        (plan_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]

