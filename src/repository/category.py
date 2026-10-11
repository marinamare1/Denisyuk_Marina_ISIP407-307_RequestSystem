from src.database.connection import get_connection

def get_all():
    """Получить все категории."""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM Categories ORDER BY id").fetchall()
    conn.close()
    return [dict(row) for row in rows]