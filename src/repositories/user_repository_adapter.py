from datetime import datetime
from typing import List

from models.user import User
from models.user_status import UserStatus
from repositories.legacy_user_storage import LegacyUserStorage
from repositories.user_repository import UserRepository
from repositories.user_type import UserType


class UserRepositoryAdapter(UserRepository):
    """
    Adapter que permite usar o sistema legado (LegacyUserStorage)
    como se fosse um UserRepository moderno.
    """

    def __init__(self, legacy_storage: LegacyUserStorage):
        self.legacy = legacy_storage

    def add(self, user: User) -> User:
        legacy_dict = {
            'name': user.name,
            'email': user.email,
            'user_type': user.user_type.value,
            'login': user.login,
            'phone': user.phone,
            'password': user.password,
            'status': user.status.value,
            'deletion_scheduled_at': user.deletion_scheduled_at.isoformat() if user.deletion_scheduled_at else None,
        }
        saved = self.legacy.save_user_legacy(legacy_dict)
        user.id = saved['id']
        return user

    def get_by_id(self, user_id: int) -> User:
        return self._dict_to_user(self.legacy.get_user_legacy(user_id))

    def update(self, user: User) -> User:
        legacy_dict = {
            'name': user.name,
            'email': user.email,
            'user_type': user.user_type.value,
            'login': user.login,
            'phone': user.phone,
            'password': user.password,
            'status': user.status.value,
            'deletion_scheduled_at': user.deletion_scheduled_at.isoformat() if user.deletion_scheduled_at else None,
        }
        self.legacy.update_user_legacy(user.id, legacy_dict)
        return user

    def list_users(self) -> List[User]:
        return [self._dict_to_user(d) for d in self.legacy.get_all_users_legacy()]

    def _dict_to_user(self, d: dict) -> User:
        deletion_at = datetime.fromisoformat(d['deletion_scheduled_at']) if d.get('deletion_scheduled_at') else None
        user = User(
            name=d['name'],
            email=d['email'],
            user_type=UserType(d['user_type']),
            login=d['login'],
            phone=d.get('phone'),
            password=d['password'],
            status=UserStatus(d.get('status', 'active')),
            deletion_scheduled_at=deletion_at,
        )
        user.id = d['id']
        return user
