import re
from typing import List

from repositories.user_repository import UserRepository, User
from schema.user_schema import UserCreateSchema
from schema.exceptions import ValidationException
from repositories.user_type import UserType

class UserControl:
    def __init__(self, repository: UserRepository):
        self._repository = repository

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
        user_type = UserType.USER if user_data.user_type.value == "user" else UserType.ADMIN
        try:
            user_data.login = self.validate_login(user_data.login)
            self.validate_password(user_data.password, user_data.name, user_data.email, user_data.login)
            new_user = User(
                name=user_data.name,
                email=user_data.email,
                user_type=user_type,
                login=user_data.login,
                phone=user_data.phone,
                password=user_data.password
            )

            return self._repository.add(new_user)
        except ValueError as e:
            raise ValueError(str(e))
        except ValidationException as e:
            raise e

    def list_users(self) -> List[User]:
        return self._repository.list_users()

