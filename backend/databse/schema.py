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

    conn.commit()
    conn.close()