import sqlite3
from typing import List

from models.user import User
from repositories.database import get_db_connection
from repositories.user_type import UserType


class UserRepository:
    """Repository for managing User persistence in the database."""

    def add(self, user: User) -> User:
        """Add a new user to the database and return it with the assigned ID."""
        try:
            with get_db_connection() as conn:
                cursor = conn.execute(
                    '''
                    INSERT INTO users (name, email, user_type, phone, login, password)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ''',
                    (user.name, user.email, user.user_type.value, user.phone, user.login, user.password)
                )
                if cursor.lastrowid is None:
                    raise IOError("Database did not return an ID for the inserted user")
                user.id = cursor.lastrowid
                return user
        except sqlite3.Error as e:
            raise IOError(f"Database error while adding user: {e}")

    def list_users(self) -> List[User]:
        """Retrieve all users from the database."""
        try:
            with get_db_connection() as conn:
                rows = conn.execute('SELECT * FROM users').fetchall()
                return [self._row_to_user(row) for row in rows]
        except sqlite3.Error as e:
            raise IOError(f"Database error while listing users: {e}")

    def _row_to_user(self, row: sqlite3.Row) -> User:
        """Convert a database row to a User object."""
        user = User(
            name=row['name'],
            email=row['email'],
            user_type=UserType(row['user_type']),
            phone=row['phone'],
            login=row['login'],
            password=row['password']
        )
        user.id = row['id']
        return user
