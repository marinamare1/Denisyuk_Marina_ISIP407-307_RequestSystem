from src.database.connection import get_connection

def get_all():
    """Получить все статусы."""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM Statuses ORDER BY id").fetchall()
    conn.close()
    return [dict(row) for row in rows]