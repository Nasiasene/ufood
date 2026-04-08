from datetime import datetime
from typing import TYPE_CHECKING, Optional

from models.user_status import UserStatus
from repositories.user_type import UserType

if TYPE_CHECKING:
    from models.user_memento import UserMemento


class User:
    id: int

    def __init__(
        self,
        name: str,
        email: str,
        user_type: UserType,
        phone: Optional[str] = None,
        login: str = "",
        password: str = "",
        status: UserStatus = UserStatus.ACTIVE,
        deletion_scheduled_at: Optional[datetime] = None,
    ):
        self.name = name
        self.email = email
        self.user_type = user_type
        self.login = login
        self.phone = phone
        self.password = password
        self.status = status
        self.deletion_scheduled_at = deletion_scheduled_at

    def save_memento(self) -> "UserMemento":
        from models.user_memento import UserMemento
        return UserMemento(user_id=self.id, name=self.name, email=self.email, login=self.login, phone=self.phone)

    def restore_from_memento(self, memento: "UserMemento") -> None:
        self.name = memento.name
        self.email = memento.email
        self.login = memento.login
        self.phone = memento.phone

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "user_type": self.user_type.value,
            "login": self.login,
            "phone": self.phone,
            "password": self.password,
            "status": self.status.value,
            "deletion_scheduled_at": self.deletion_scheduled_at.isoformat() if self.deletion_scheduled_at else None,
        }

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}', email='{self.email}', status={self.status.value})"
