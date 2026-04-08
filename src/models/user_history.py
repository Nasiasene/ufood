from collections import defaultdict
from typing import Dict, List, Optional

from models.user_memento import UserMemento


class UserHistory:
    """Caretaker do padrão Memento. Mantém uma pilha de snapshots por usuário."""

    def __init__(self):
        self._stacks: Dict[int, List[UserMemento]] = defaultdict(list)

    def push(self, memento: UserMemento) -> None:
        self._stacks[memento.user_id].append(memento)

    def pop(self, user_id: int) -> Optional[UserMemento]:
        stack = self._stacks.get(user_id)
        if not stack:
            return None
        return stack.pop()

    def has_history(self, user_id: int) -> bool:
        return bool(self._stacks.get(user_id))
