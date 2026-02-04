import os
import sqlite3
from contextlib import contextmanager
from typing import Generator

DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'ufood.db')


def get_connection() -> sqlite3.Connection:
    """Get a database connection, creating the database directory if needed."""
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def get_db_connection() -> Generator[sqlite3.Connection, None, None]:
    """Context manager for database connections with automatic cleanup."""
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except sqlite3.Error:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    """Initialize database tables."""
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                user_type TEXT NOT NULL,
                phone TEXT,
                login TEXT,
                password TEXT
            )
        ''')


# Initialize on import
init_db()
