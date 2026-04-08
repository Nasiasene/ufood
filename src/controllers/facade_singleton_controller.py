import re
from typing import Any, Dict, List

from commands.command_bus import CommandBus
from commands.user_commands import EditUserCommand, ListUsersCommand, SignUpUserCommand
from controllers.templates.sign_up_operation_template import SignUpOperationTemplate
from models.user import User
from models.user_history import UserHistory
from repositories.user_repository import UserRepository
from schema.exceptions import ValidationException
from schema.user_schema import UserCreateSchema, UserUpdateSchema


class FacadeSingletonController:
    _instance = None

    def __new__(cls, user_repository: UserRepository):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_once(user_repository)
        return cls._instance

    def _init_once(self, user_repository: UserRepository) -> None:
        self._repository = user_repository
        self._command_bus = CommandBus()
        self._user_history = UserHistory()
        self._sign_up_operation = SignUpOperationTemplate(
            repository=user_repository,
            validate_login=self._validate_login,
            validate_password=self._validate_password,
        )

    def _validate_login(self, login: str) -> str:
        if len(login) > 12 or len(login) < 1:
            raise ValidationException("O login deve ter entre 1 e 12 caracteres.")
        if login.strip() == "":
            raise ValidationException("Login não pode ser vazio ou apenas espaços em branco")
        if any(char.isdigit() for char in login):
            raise ValidationException("Login não pode conter números")
        return login.strip()

    def _validate_password(self, password: str, name: str, email: str, login: str) -> None:
        if len(password) < 8 or len(password) > 128:
            raise ValidationException("A senha deve ter entre 8 e 128 caracteres.")
        char_types = [
            bool(re.search(r"[A-Z]", password)),
            bool(re.search(r"[a-z]", password)),
            bool(re.search(r"[0-9]", password)),
            bool(re.search(r"[!@#$%^&*()_+\-=\[\]{}|']", password)),
        ]
        if sum(char_types) < 3:
            raise ValidationException(
                "A senha deve conter pelo menos três dos seguintes tipos de caracteres: "
                "maiúsculas, minúsculas, números e caracteres não alfanuméricos (! @ # $ % ^ & * ( ) _ + - = [ ] { } | ')."
            )
        if password == name or password == email or password == login:
            raise ValidationException("A senha não pode ser idêntica ao nome, ao endereço de e-mail ou ao login.")

    def sign_up(self, user_data: UserCreateSchema) -> User:
        command = SignUpUserCommand(self._sign_up_operation.execute, user_data)
        return self._command_bus.dispatch(command)

    def list_users(self) -> List[User]:
        command = ListUsersCommand(self._repository.list_users)
        return self._command_bus.dispatch(command)

    def edit_user(self, user_id: int, user_data: UserUpdateSchema) -> User:
        user = self._repository.get_by_id(user_id)
        self._user_history.push(user.save_memento())
        command = EditUserCommand(self._apply_edit, user_id, user_data)
        return self._command_bus.dispatch(command)

    def undo_last_edit(self, user_id: int) -> User:
        memento = self._user_history.pop(user_id)
        if memento is None:
            raise ValueError(f"Nenhum histórico de edição para o usuário {user_id}.")
        user = self._repository.get_by_id(user_id)
        user.restore_from_memento(memento)
        return self._repository.update(user)

    def _apply_edit(self, user_id: int, user_data: UserUpdateSchema) -> User:
        user = self._repository.get_by_id(user_id)
        if user_data.name is not None:
            user.name = user_data.name.strip()
        if user_data.email is not None:
            user.email = user_data.email.strip().lower()
        if user_data.login is not None:
            user.login = self._validate_login(user_data.login)
        if user_data.phone is not None:
            user.phone = user_data.phone
        return self._repository.update(user)

    def command_history(self) -> List[Dict[str, Any]]:
        return self._command_bus.get_history()

    def count_entities(self) -> int:
        return len(self._repository.list_users())
