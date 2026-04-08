from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class UserMemento:
    """Snapshot imutável do estado editável de um User (Memento)."""
    user_id: int
    name: str
    email: str
    login: str
    phone: Optional[str]
