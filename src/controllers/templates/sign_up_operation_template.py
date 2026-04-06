from typing import Callable

from models.user import User
from repositories.user_repository import UserRepository
from repositories.user_type import UserType
from schema.user_schema import UserCreateSchema

from controllers.templates.user_operation_template import UserOperationTemplate


class SignUpOperationTemplate(UserOperationTemplate):
    def __init__(
        self,
        repository: UserRepository,
        validate_login: Callable[[str], str],
        validate_password: Callable[[str, str, str, str], None],
    ):
        self._repository = repository
        self._validate_login = validate_login
        self._validate_password = validate_password

    def prepare(self, user_data: UserCreateSchema) -> UserCreateSchema:
        user_data.login = self._validate_login(user_data.login)
        user_data.email = user_data.email.strip().lower()
        user_data.name = user_data.name.strip()
        return user_data

    def validate(self, user_data: UserCreateSchema) -> None:
        self._validate_password(
            user_data.password,
            user_data.name,
            user_data.email,
            user_data.login,
        )

    def create_entity(self, user_data: UserCreateSchema) -> User:
        user_type = UserType.USER if user_data.user_type.value == "user" else UserType.ADMIN
        return User(
            name=user_data.name,
            email=user_data.email,
            user_type=user_type,
            login=user_data.login,
            phone=user_data.phone,
            password=user_data.password,
        )

    def persist(self, user: User) -> User:
        return self._repository.add(user)
