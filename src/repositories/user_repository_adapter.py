from typing import List
from models.user import User
from repositories.user_repository import UserRepository
from repositories.legacy_user_storage import LegacyUserStorage
from repositories.user_type import UserType

class UserRepositoryAdapter(UserRepository):
    """
    Adapter que permite usar o sistema legado (LegacyUserStorage)
    como se fosse um UserRepository moderno.

    O Adapter converte as chamadas do UserRepository para o formato esperado pelo LegacyUserStorage,
    e também converte os dados de volta para o formato do User quando necessário.

    Para testar este adapter, basta criar uma instância de LegacyUserStorage e passar para o UserRepositoryAdapter.
    Exemplo:
    legacy_storage = LegacyUserStorage()
    user_repo = UserRepositoryAdapter(legacy_storage)
    facade = FacadeSingletonControl(user_repo)
    control = facade.user_control

    # Cria um usuário
    payload = UserCreateSchema(
        name='Ana',
        email='ana@example.com',
        user_type='user',
        login='ana',
        phone='123',
        password='SenhaForte123!'
    )
    created = control.sign_up(payload)
    """
    def __init__(self, legacy_storage: LegacyUserStorage):
        self.legacy = legacy_storage

    def add(self, user: User) -> User:
        # Converte User para dict no formato esperado pelo legado
        legacy_dict = {
            'name': user.name,
            'email': user.email,
            'user_type': user.user_type.value,
            'login': user.login,
            'phone': user.phone,
            'password': user.password,
        }
        saved = self.legacy.save_user_legacy(legacy_dict)
        user.id = saved['id']
        return user

    def get_by_id(self, user_id: int) -> User:
        legacy_dict = self.legacy.get_user_legacy(user_id)
        user = User(
            name=legacy_dict['name'],
            email=legacy_dict['email'],
            user_type=UserType(legacy_dict['user_type']),
            login=legacy_dict['login'],
            phone=legacy_dict.get('phone'),
            password=legacy_dict['password'],
        )
        user.id = legacy_dict['id']
        return user

    def update(self, user: User) -> User:
        legacy_dict = {
            'name': user.name,
            'email': user.email,
            'user_type': user.user_type.value,
            'login': user.login,
            'phone': user.phone,
            'password': user.password,
        }
        self.legacy.update_user_legacy(user.id, legacy_dict)
        return user

    def list_users(self) -> List[User]:
        users = []
        for legacy_dict in self.legacy.get_all_users_legacy():
            user = User(
                name=legacy_dict['name'],
                email=legacy_dict['email'],
                user_type=UserType(legacy_dict['user_type']),
                login=legacy_dict['login'],
                phone=legacy_dict.get('phone'),
                password=legacy_dict['password'],
            )
            user.id = legacy_dict['id']
            users.append(user)
        return users
