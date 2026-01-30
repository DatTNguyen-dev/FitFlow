from .connection import get_connection

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY, 
        create_at TEXT NOT NULL
                   )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_profile (
        user_id TEXT PRIMARY KEY,
        fitness_level TEXT,
        age INTERGER,
        height_cm REAL,
        weight_kg REAL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS training_plans (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        start_date TEXT,
        end_date TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS training_tasks (
        id TEXT PRIMARY KEY,
        plan_id TEXT NOT NULL,
        name TEXT,
        duration_minutes INTEGER,
        scheduled_date TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS task_completion (
        task_id TEXT PRIMARY KEY,
        completed INTEGER,
        completed_at TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()