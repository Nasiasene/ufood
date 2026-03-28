from abc import ABC, abstractmethod
from repositories.user_repository import UserRepository

#Aplicação do Padrão Abstract Factory para selecionar o repositórios de dados.
#O RepositoryFactory define a interface para criar repositórios;
#E as implementações concretas (InMemoryRepositoryFactory e SqliteRepositoryFactory),
#criam repositórios específicos para cada tipo de armazenamento.

class RepositoryFactory(ABC):
    """Abstract Factory para criar repositórios.
    
    Define a interface para criação de repositórios concretos.
    Cada implementação concreta cria um conjunto específico de repositórios
    (ex: em memória, SQLite, etc).
    """

    @abstractmethod
    def create_user_repository(self) -> UserRepository:
        """Cria um repositório de usuários."""
        pass


class InMemoryRepositoryFactory(RepositoryFactory):
    """Factory que cria repositórios em memória.
    
    Os dados são perdidos quando a aplicação é interrompida.
    """

    def create_user_repository(self) -> UserRepository:
        from repositories.user_repository import InMemoryUserRepository
        return InMemoryUserRepository()


class SqliteRepositoryFactory(RepositoryFactory):
    """Factory que cria repositórios com persistência em SQLite.
    
    Os dados são armazenados em banco de dados local.
    """

    def create_user_repository(self) -> UserRepository:
        from repositories.user_repository import SqliteUserRepository
        return SqliteUserRepository()


def get_repository_factory(storage_mode: str) -> RepositoryFactory:
    """Factory helper que seleciona o tipo correto de factory.
    
    Args:
        storage_mode: "memory" para em memória ou "sqlite" para banco de dados.
        
    Returns:
        RepositoryFactory: Uma factory concreta apropriada.
        
    Raises:
        ValueError: Se storage_mode não for um valor válido.
    """
    if storage_mode == "sqlite":
        return SqliteRepositoryFactory()
    elif storage_mode == "memory":
        return InMemoryRepositoryFactory()
    else:
        raise ValueError(f"Storage mode inválido: {storage_mode}. Use 'sqlite' ou 'memory'.")
