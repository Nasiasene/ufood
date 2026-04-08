from typing import Callable, List

from commands.base_command import Command
from models.user import User
from schema.user_schema import UserCreateSchema, UserUpdateSchema


class SignUpUserCommand(Command):
    def __init__(self, sign_up_action: Callable[[UserCreateSchema], User], user_data: UserCreateSchema):
        self._sign_up_action = sign_up_action
        self._user_data = user_data

    def execute(self) -> User:
        return self._sign_up_action(self._user_data)


class ListUsersCommand(Command):
    def __init__(self, list_action: Callable[[], List[User]]):
        self._list_action = list_action

    def execute(self) -> List[User]:
        return self._list_action()


class EditUserCommand(Command):
    def __init__(self, edit_action: Callable[[int, UserUpdateSchema], User], user_id: int, user_data: UserUpdateSchema):
        self._edit_action = edit_action
        self._user_id = user_id
        self._user_data = user_data

    def execute(self) -> User:
        return self._edit_action(self._user_id, self._user_data)
