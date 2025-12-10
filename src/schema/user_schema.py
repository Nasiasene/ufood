from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class TipoUsuarioSchema(str, Enum):
    VENDEDOR = "vendedor"
    CLIENTE = "cliente"


class UserCreateSchema(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100, description= "Nome do usuário")
    email: str = Field(..., description= "Email do usuário")
    tipo: TipoUsuarioSchema = Field(..., description= "Tipo do usuário: vendedor ou cliente")
    telefone: Optional[str] = Field(None, max_length=20, description= "Telefone do usuário")

    class Config:
        json_schema_extra = { # exemplo p docs
            "example": {
                "nome": "João Silva",
                "email": "joao.silva@universidade.edu.br",
                "tipo": "cliente",
                "telefone": "(11) 98765-4321"
            }
        }


class UserResponseSchema(BaseModel):
    id: int
    nome: str
    email: str
    tipo: str
    telefone: Optional[str] = None

    class Config:
        json_schema_extra = { # exemplo p docs
            "example": {
                "id": 1,
                "nome": "João Silva",
                "email": "joao.silva@universidade.edu.br",
                "tipo": "cliente",
                "telefone": "(11) 98765-4321"
            }
        }

