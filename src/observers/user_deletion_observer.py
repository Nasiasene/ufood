from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from models.user import User
from models.user_status import UserStatus


class UserDeletionObserver(ABC):
    """Interface do padrão Observer para eventos de exclusão de usuário."""

    @abstractmethod
    def on_user_deleted(self, user: User) -> None:
        pass


class DeletionLogObserver(UserDeletionObserver):
    """Registra no log quando um usuário é marcado para exclusão."""

    def on_user_deleted(self, user: User) -> None:
        print(f"[LOG] Usuário '{user.name}' (id={user.id}) marcado para exclusão permanente em 30 dias.")


class ScheduledDeletionObserver(UserDeletionObserver):
    """Marca o usuário como PENDING_DELETION e agenda a data de remoção definitiva."""

    GRACE_PERIOD_DAYS = 30

    def on_user_deleted(self, user: User) -> None:
        user.status = UserStatus.PENDING_DELETION
        user.deletion_scheduled_at = datetime.now() + timedelta(days=self.GRACE_PERIOD_DAYS)
