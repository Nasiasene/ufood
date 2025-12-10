from enum import Enum
from typing import Optional


class TipoUsuario(Enum):
    VENDEDOR = "vendedor"
    CLIENTE = "cliente"


class User:
    def __init__(self, id: int, nome: str, email: str, tipo: TipoUsuario, telefone: Optional[str] = None):
        self.id = id
        self.nome = nome
        self.email = email
        self.tipo = tipo
        self.telefone = telefone

    def to_dict(self): # p/ facilitar o retorno, convertendo para um dicionário
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "tipo": self.tipo.value,
            "telefone": self.telefone
        }

    def __repr__(self): # log em uma linha como string
        return f"User(id={self.id}, nome='{self.nome}', email='{self.email}', tipo={self.tipo.value})"

