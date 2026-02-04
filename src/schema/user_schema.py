from pydantic import BaseModel, Field
from typing import Optional
import re

from repositories.user_type import UserType
from schema.exceptions import ValidationException


class UserCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description= "Nome do usuário")
    email: str = Field(..., description= "Email do usuário")
    user_type: UserType = Field(..., description= "Tipo do usuário: user ou admin")
    login: str = Field(..., description= "Login do usuário")
    phone: Optional[str] = Field(None, max_length=20, description= "Telefone do usuário")
    password: str = Field(..., description="Senha do usuário")

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