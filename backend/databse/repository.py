import uuid
from datetime import datetime
from .connection import get_connection

def create_user():
    conn = get_connection
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