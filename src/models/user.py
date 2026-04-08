from typing import TYPE_CHECKING, Optional

from repositories.user_type import UserType

if TYPE_CHECKING:
    from models.user_memento import UserMemento


class User:
    id: int

    def __init__(self, name: str, email: str, user_type: UserType, phone: Optional[str] = None, login: str = "", password: str = ""):
        self.name = name
        self.email = email
        self.user_type = user_type
        self.login = login
        self.phone = phone
        self.password = password

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
            "password": self.password
        }

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}', email='{self.email}', user_type={self.user_type.value}, login='{self.login}')"

