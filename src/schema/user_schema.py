from pydantic import BaseModel, Field
from typing import Optional

from repositories.user_type import UserType


class UserCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description= "Nome do usuário")
    email: str = Field(..., description= "Email do usuário")
    user_type: UserType = Field(..., description= "Tipo do usuário: user ou admin")
    phone: Optional[str] = Field(None, max_length=20, description= "Telefone do usuário")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Davi Nasiasene",
                "email": "davi.nasiasene@gmail.com",
                "user_type": "user",
                "phone": "(83) 99999-9999"
            }
        }


class UserResponseSchema(BaseModel):
    id: int
    name: str
    email: str
    user_type: str
    phone: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Davi Nasiasene",
                "email": "davi.nasiasene@gmail.com",
                "user_type": "user",
                "phone": "(83) 99999-9999"
            }
        }