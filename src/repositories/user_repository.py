import sqlite3
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from models.user import User
from models.user_status import UserStatus
from repositories.user_type import UserType


class UserRepository(ABC):
    """Abstract interface for User persistence."""

    @abstractmethod
    def add(self, user: User) -> User:
        ...

    @abstractmethod
    def list_users(self) -> List[User]:
        ...

    @abstractmethod
    def get_by_id(self, user_id: int) -> User:
        ...

    @abstractmethod
    def update(self, user: User) -> User:
        ...


class InMemoryUserRepository(UserRepository):
    """Stores users in RAM. Data is lost when the application stops."""

    def __init__(self):
        self._users: List[User] = []
        self._next_id = 0

    def add(self, user: User) -> User:
        self._next_id += 1
        user.id = self._next_id
        self._users.append(user)
        return user

    def list_users(self) -> List[User]:
        return list(self._users)

    def get_by_id(self, user_id: int) -> User:
        for user in self._users:
            if user.id == user_id:
                return user
        raise ValueError(f"Usuário {user_id} não encontrado.")

    def update(self, user: User) -> User:
        for i, u in enumerate(self._users):
            if u.id == user.id:
                self._users[i] = user
                return user
        raise ValueError(f"Usuário {user.id} não encontrado.")


class SqliteUserRepository(UserRepository):
    """Stores users in a local SQLite database. Data persists across restarts."""

    def add(self, user: User) -> User:
        from repositories.database import get_db_connection

        try:
            with get_db_connection() as conn:
                cursor = conn.execute(
                    '''
                    INSERT INTO users (name, email, user_type, phone, login, password, status, deletion_scheduled_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''',
                    (user.name, user.email, user.user_type.value, user.phone, user.login, user.password,
                     user.status.value, user.deletion_scheduled_at.isoformat() if user.deletion_scheduled_at else None)
                )
                if cursor.lastrowid is None:
                    raise IOError("Database did not return an ID for the inserted user")
                user.id = cursor.lastrowid
                return user
        except sqlite3.Error as e:
            raise IOError(f"Database error while adding user: {e}")

    def list_users(self) -> List[User]:
        from repositories.database import get_db_connection

        try:
            with get_db_connection() as conn:
                rows = conn.execute('SELECT * FROM users').fetchall()
                return [self._row_to_user(row) for row in rows]
        except sqlite3.Error as e:
            raise IOError(f"Database error while listing users: {e}")

    def get_by_id(self, user_id: int) -> User:
        from repositories.database import get_db_connection

        try:
            with get_db_connection() as conn:
                row = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
                if row is None:
                    raise ValueError(f"Usuário {user_id} não encontrado.")
                return self._row_to_user(row)
        except sqlite3.Error as e:
            raise IOError(f"Database error while fetching user: {e}")

    def update(self, user: User) -> User:
        from repositories.database import get_db_connection

        try:
            with get_db_connection() as conn:
                conn.execute(
                    'UPDATE users SET name=?, email=?, user_type=?, phone=?, login=?, password=?, status=?, deletion_scheduled_at=? WHERE id=?',
                    (user.name, user.email, user.user_type.value, user.phone, user.login, user.password,
                     user.status.value, user.deletion_scheduled_at.isoformat() if user.deletion_scheduled_at else None, user.id)
                )
                return user
        except sqlite3.Error as e:
            raise IOError(f"Database error while updating user: {e}")

    def _row_to_user(self, row: sqlite3.Row) -> User:
        deletion_at = datetime.fromisoformat(row['deletion_scheduled_at']) if row['deletion_scheduled_at'] else None
        user = User(
            name=row['name'],
            email=row['email'],
            user_type=UserType(row['user_type']),
            phone=row['phone'],
            login=row['login'],
            password=row['password'],
            status=UserStatus(row['status']) if row['status'] else UserStatus.ACTIVE,
            deletion_scheduled_at=deletion_at,
        )
        user.id = row['id']
        return user
