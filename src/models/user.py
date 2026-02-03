from typing import Optional
from repositories.user_type import UserType

class User:
    id: int
    
    def __init__(self, name: str, email: str, user_type: UserType, phone: Optional[str] = None, login: str = "", password: str = ""):
        self.name = name
        self.email = email
        self.user_type = user_type
        self.login = login
        self.phone = phone
        self.password = password

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

