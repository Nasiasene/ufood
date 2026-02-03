from pydantic import BaseModel, Field
from typing import Optional
import re

from repositories.user_type import UserType


class UserCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description= "Nome do usuário")
    email: str = Field(..., description= "Email do usuário")
    user_type: UserType = Field(..., description= "Tipo do usuário: user ou admin")
    login: str = Field(..., min_length=1, max_length=12, description= "Login do usuário")
    phone: Optional[str] = Field(None, max_length=20, description= "Telefone do usuário")
    password: str = Field(..., min_length=8, max_length=128, description="Senha do usuário")

    def validate_login(self):
        if self.login.strip() is None:
            raise ValueError("Login não pode ser vazio ou apenas espaços em branco")
        if any(char.isdigit() for char in self.login):
            raise ValueError("Login não pode conter números")
        
        self.login = self.login.strip()
    
    def validate_password(self):
        char_types = [
            bool(re.search(r"[A-Z]", self.password)),  # Uppercase
            bool(re.search(r"[a-z]", self.password)),  # Lowercase
            bool(re.search(r"[0-9]", self.password)),  # Numbers
            bool(re.search(r"[!@#$%^&*()_+\-=\[\]{}|']", self.password))  # Special characters
        ]

        if sum(char_types) < 3:
            raise ValueError(
                "A senha deve conter pelo menos três dos seguintes tipos de caracteres: "
                "maiúsculas, minúsculas, números e caracteres não alfanuméricos (! @ # $ % ^ & * ( ) _ + - = [ ] { } | ')."
            )
    
        # Check if the password is identical to the name or email
        if self.password == self.name or self.password == self.email or self.password == self.login:
            raise ValueError("A senha não pode ser idêntica ao nome, ao endereço de e-mail ou ao login.")


    class Config:
        json_schema_extra = {
            "example": {
                "name": "Davi Nasiasene",
                "email": "davi.nasiasene@gmail.com",
                "login": "nasiasene",
                "user_type": "user",
                "phone": "(83) 99999-9999",
                "password": "SenhaForte123!"
            }
        }


class UserResponseSchema(BaseModel):
    id: int
    name: str
    email: str
    login: str
    user_type: str
    phone: Optional[str] = None
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Davi Nasiasene",
                "email": "davi.nasiasene@gmail.com",
                "user_type": "user",
                "login": "nasiasene",
                "phone": "(83) 99999-9999",
                "password": "SenhaForte123!"
            }
        }