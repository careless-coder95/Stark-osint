import sqlite3
import logging
from config import DB_PATH

logger = logging.getLogger(__name__)


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database and create tables if they don't exist."""
    import os
    os.makedirs("database", exist_ok=True)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id       INTEGER PRIMARY KEY,
            name          TEXT,
            username      TEXT,
            search_count  INTEGER DEFAULT 0,
            joined_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    logger.info("Database initialized.")


def upsert_user(user_id: int, name: str, username: str):
    """Insert or update user record."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (user_id, name, username)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            name     = excluded.name,
            username = excluded.username
    """, (user_id, name, username or ""))
    conn.commit()
    conn.close()


def increment_search(user_id: int):
    """Increment the search count for a user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users SET search_count = search_count + 1
        WHERE user_id = ?
    """, (user_id,))
    conn.commit()
    conn.close()


def get_user(user_id: int) -> dict | None:
    """Fetch user record by user_id."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None


def get_total_users() -> int:
    """Return total number of registered users."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()
    return count
