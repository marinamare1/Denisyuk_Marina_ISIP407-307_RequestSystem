from src.database.connection import get_connection
from src.domain.models import Request

def get_all():
    """Получить все заявки."""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM Requests ORDER BY id").fetchall()
    conn.close()
    return [Request(**dict(row)) for row in rows]

def get_by_id(request_id):
    """Получить заявку по идентификатору."""
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM Requests WHERE id = ?", (request_id,)
    ).fetchone()
    conn.close()
    return Request(**dict(row)) if row else None

def search(query):
    """Поиск заявок по номеру, теме или описанию."""
    conn = get_connection()
    like = f"%{query}%"
    rows = conn.execute(
        """SELECT * FROM Requests
           WHERE request_number LIKE ?
              OR topic LIKE ?
              OR description LIKE ?
           ORDER BY id""",
        (like, like, like)
    ).fetchall()
    conn.close()
    return [Request(**dict(row)) for row in rows]

def filter_by(status_id=None, category_id=None):
    """Фильтрация заявок по статусу и категории."""
    conn = get_connection()
    sql = "SELECT * FROM Requests WHERE 1=1"
    params = []
    if status_id:
        sql += " AND status_id = ?"
        params.append(status_id)
    if category_id:
        sql += " AND category_id = ?"
        params.append(category_id)
    sql += " ORDER BY id"
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return [Request(**dict(row)) for row in rows]

def create(request):
    """Создать новую заявку."""
    conn = get_connection()
    cur = conn.execute(
        """INSERT INTO Requests
           (request_number, topic, description, priority,
            category_id, status_id, requester_id, assignee_id)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (request.request_number, request.topic, request.description,
         request.priority, request.category_id, request.status_id,
         request.requester_id, request.assignee_id)
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id

def update(request_id, topic=None, description=None,
           category_id=None, priority=None, status_id=None,
           assignee_id=None):
    """Обновить поля заявки."""
    conn = get_connection()
    fields = []
    params = []
    if topic is not None:
        fields.append("topic = ?")
        params.append(topic)
    if description is not None:
        fields.append("description = ?")
        params.append(description)
    if category_id is not None:
        fields.append("category_id = ?")
        params.append(category_id)
    if priority is not None:
        fields.append("priority = ?")
        params.append(priority)
    if status_id is not None:
        fields.append("status_id = ?")
        params.append(status_id)
    if assignee_id is not None:
        fields.append("assignee_id = ?")
        params.append(assignee_id)
    if not fields:
        conn.close()
        return
    params.append(request_id)
    sql = f"UPDATE Requests SET {', '.join(fields)} WHERE id = ?"
    conn.execute(sql, params)
    conn.commit()
    conn.close()

def delete(request_id):
    """Удалить заявку."""
    conn = get_connection()
    conn.execute("DELETE FROM Requests WHERE id = ?", (request_id,))
    conn.commit()
    conn.close()

def get_last_number():
    """Получить последний номер заявки для генерации нового."""
    conn = get_connection()
    row = conn.execute(
        "SELECT request_number FROM Requests ORDER BY id DESC LIMIT 1"
    ).fetchone()
    conn.close()
    return row["request_number"] if row else None