"""
Database layer demonstrating SQL injection prevention.

SECURITY BEST PRACTICE: Always use parameterized queries. Never concatenate
user input into SQL strings.
"""

import sqlite3
from contextlib import contextmanager


DATABASE_PATH = "app.db"


def init_db():
    """Initialize the database with a users table."""
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                role TEXT NOT NULL DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)


@contextmanager
def get_db():
    """Context manager for database connections."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def find_user_by_username(username: str) -> dict | None:
    """
    Find a user by username using parameterized queries.

    SECURE: Uses ? placeholder — immune to SQL injection.
    """
    with get_db() as db:
        row = db.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        return dict(row) if row else None


def find_user_by_id(user_id: int) -> dict | None:
    """Find a user by ID using parameterized queries."""
    with get_db() as db:
        row = db.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        return dict(row) if row else None


def create_user(username: str, password_hash: str, email: str) -> int:
    """
    Create a new user with parameterized insert.

    SECURE: All values are bound parameters, not string-interpolated.
    """
    with get_db() as db:
        cursor = db.execute(
            "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
            (username, password_hash, email),
        )
        return cursor.lastrowid


def get_posts_for_user(user_id: int) -> list[dict]:
    """Get all posts for a user using parameterized query."""
    with get_db() as db:
        rows = db.execute(
            "SELECT * FROM posts WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,),
        ).fetchall()
        return [dict(row) for row in rows]


def create_post(user_id: int, title: str, content: str) -> int:
    """Create a post with parameterized insert."""
    with get_db() as db:
        cursor = db.execute(
            "INSERT INTO posts (user_id, title, content) VALUES (?, ?, ?)",
            (user_id, title, content),
        )
        return cursor.lastrowid
