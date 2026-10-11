import sqlite3
import os

DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "..", "..", "docs", "database", "request_system.db"
)

def get_connection():
    """Открывает соединение с базой данных SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn