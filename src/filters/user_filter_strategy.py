from abc import ABC, abstractmethod
from typing import List

from models.user import User
from repositories.user_type import UserType


class UserFilterStrategy(ABC):
    """Interface do padrão Strategy para filtros de listagem de usuários."""

    @abstractmethod
    def apply(self, users: List[User]) -> List[User]:
        pass


class NoFilter(UserFilterStrategy):
    """Estratégia nula — retorna todos os usuários sem filtrar."""

    def apply(self, users: List[User]) -> List[User]:
        return users


class FilterByName(UserFilterStrategy):
    def __init__(self, name: str):
        self._name = name.lower()

    def apply(self, users: List[User]) -> List[User]:
        return [u for u in users if self._name in u.name.lower()]


class FilterByEmail(UserFilterStrategy):
    def __init__(self, email: str):
        self._email = email.lower()

    def apply(self, users: List[User]) -> List[User]:
        return [u for u in users if self._email in u.email.lower()]


class FilterByUserType(UserFilterStrategy):
    def __init__(self, user_type: UserType):
        self._user_type = user_type

    def apply(self, users: List[User]) -> List[User]:
        return [u for u in users if u.user_type == self._user_type]


class CompositeFilter(UserFilterStrategy):
    """Combina múltiplas estratégias em série (lógica AND)."""

    def __init__(self, strategies: List[UserFilterStrategy]):
        self._strategies = strategies

    def apply(self, users: List[User]) -> List[User]:
        result = users
        for strategy in self._strategies:
            result = strategy.apply(result)
        return result
