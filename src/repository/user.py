from src.database.connection import get_connection

def get_all():
    """Получить всех пользователей."""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM Users ORDER BY id").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_by_id(user_id):
    """Получить пользователя по id."""
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM Users WHERE id = ?", (user_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None