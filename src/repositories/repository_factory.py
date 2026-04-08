from abc import ABC, abstractmethod

from repositories.store_repository import StoreRepository
from repositories.user_repository import UserRepository


class RepositoryFactory(ABC):
    """Abstract Factory para criar repositórios de dados."""

    @abstractmethod
    def create_user_repository(self) -> UserRepository:
        pass

    @abstractmethod
    def create_store_repository(self) -> StoreRepository:
        pass


class InMemoryRepositoryFactory(RepositoryFactory):
    def create_user_repository(self) -> UserRepository:
        from repositories.user_repository import InMemoryUserRepository
        return InMemoryUserRepository()

    def create_store_repository(self) -> StoreRepository:
        from repositories.store_repository import InMemoryStoreRepository
        return InMemoryStoreRepository()


class SqliteRepositoryFactory(RepositoryFactory):
    def create_user_repository(self) -> UserRepository:
        from repositories.user_repository import SqliteUserRepository
        return SqliteUserRepository()

    def create_store_repository(self) -> StoreRepository:
        from repositories.store_repository import SqliteStoreRepository
        return SqliteStoreRepository()


class LegacyRepositoryFactory(RepositoryFactory):
    """Usuários usam o sistema legado; lojas usam memória (legado não suporta lojas)."""

    def create_user_repository(self) -> UserRepository:
        from repositories.legacy_user_storage import LegacyUserStorage
        from repositories.user_repository_adapter import UserRepositoryAdapter
        return UserRepositoryAdapter(LegacyUserStorage())

    def create_store_repository(self) -> StoreRepository:
        from repositories.store_repository import InMemoryStoreRepository
        return InMemoryStoreRepository()


def get_repository_factory(storage_mode: str) -> RepositoryFactory:
    if storage_mode == "sqlite":
        return SqliteRepositoryFactory()
    elif storage_mode == "memory":
        return InMemoryRepositoryFactory()
    elif storage_mode == "legacy":
        return LegacyRepositoryFactory()
    else:
        raise ValueError(f"Storage mode inválido: {storage_mode}. Use 'sqlite', 'memory' ou 'legacy'.")
