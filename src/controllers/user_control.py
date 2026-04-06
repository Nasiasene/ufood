import re
from typing import List

from commands.command_bus import CommandBus
from commands.user_commands import SignUpUserCommand, ListUsersCommand
from models.user import User
from repositories.user_repository import UserRepository
from schema.user_schema import UserCreateSchema
from schema.exceptions import ValidationException
from repositories.user_type import UserType
from controllers.templates.sign_up_operation_template import SignUpOperationTemplate

class UserControl:
    def __init__(self, repository: UserRepository):
        self._repository = repository
        self._command_bus = CommandBus()
        self._sign_up_operation = SignUpOperationTemplate(
            repository=self._repository,
            validate_login=self.validate_login,
            validate_password=self.validate_password,
        )

    def validate_login(self, login: str):
        if len(login) > 12 or len(login) < 1:
            raise ValidationException("O login deve ter entre 1 e 12 caracteres.")
        if login.strip() == "":
            raise ValidationException("Login não pode ser vazio ou apenas espaços em branco")
        if any(char.isdigit() for char in login):
            raise ValidationException("Login não pode conter números")
        return login.strip()

    def validate_password(self, password: str, name: str, email: str, login: str):
        if len(password) < 8 or len(password) > 128:
            raise ValidationException("A senha deve ter entre 8 e 128 caracteres.")
        char_types = [
            bool(re.search(r"[A-Z]", password)),  # Uppercase
            bool(re.search(r"[a-z]", password)),  # Lowercase
            bool(re.search(r"[0-9]", password)),  # Numbers
            bool(re.search(r"[!@#$%^&*()_+\-=\[\]{}|']", password))  # Special characters
        ]

        if sum(char_types) < 3:
            raise ValidationException(
                "A senha deve conter pelo menos três dos seguintes tipos de caracteres: "
                "maiúsculas, minúsculas, números e caracteres não alfanuméricos (! @ # $ % ^ & * ( ) _ + - = [ ] { } | ')."
            )
        if password == name or password == email or password == login:
            raise ValidationException("A senha não pode ser idêntica ao nome, ao endereço de e-mail ou ao login.")

    def sign_up(self, user_data: UserCreateSchema):
        try:
            command = SignUpUserCommand(self._sign_up_operation.execute, user_data)
            return self._command_bus.dispatch(command)
        except ValueError as e:
            raise ValueError(str(e))
        except ValidationException as e:
            raise e

    def list_users(self) -> List[User]:
        command = ListUsersCommand(self._repository.list_users)
        return self._command_bus.dispatch(command)

    def command_history(self):
        return self._command_bus.get_history()

