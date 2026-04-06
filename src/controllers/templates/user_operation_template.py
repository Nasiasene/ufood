from abc import ABC, abstractmethod

from models.user import User
from schema.user_schema import UserCreateSchema


class UserOperationTemplate(ABC):
    def execute(self, user_data: UserCreateSchema) -> User:
        prepared_data = self.prepare(user_data)
        self.validate(prepared_data)
        user_entity = self.create_entity(prepared_data)
        persisted_user = self.persist(user_entity)
        self.after_persist(persisted_user)
        return persisted_user

    def prepare(self, user_data: UserCreateSchema) -> UserCreateSchema:
        return user_data

    @abstractmethod
    def validate(self, user_data: UserCreateSchema) -> None:
        pass

    @abstractmethod
    def create_entity(self, user_data: UserCreateSchema) -> User:
        pass

    @abstractmethod
    def persist(self, user: User) -> User:
        pass

    def after_persist(self, user: User) -> None:
        return None
