from typing import List

from models.user import User
from observers.user_deletion_observer import UserDeletionObserver


class UserDeletionPublisher:
    """Subject do padrão Observer. Notifica todos os observers registrados quando um usuário é excluído."""

    def __init__(self):
        self._observers: List[UserDeletionObserver] = []

    def subscribe(self, observer: UserDeletionObserver) -> None:
        self._observers.append(observer)

    def unsubscribe(self, observer: UserDeletionObserver) -> None:
        self._observers.remove(observer)

    def notify(self, user: User) -> None:
        for observer in self._observers:
            observer.on_user_deleted(user)
