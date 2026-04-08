from typing import Callable, List

from commands.base_command import Command
from models.store import Store
from schema.store_schema import StoreCreateSchema, StoreUpdateSchema


class CreateStoreCommand(Command):
    def __init__(self, action: Callable[[StoreCreateSchema], Store], data: StoreCreateSchema):
        self._action = action
        self._data = data

    def execute(self) -> Store:
        return self._action(self._data)


class ListStoresCommand(Command):
    def __init__(self, action: Callable[[], List[Store]]):
        self._action = action

    def execute(self) -> List[Store]:
        return self._action()


class EditStoreCommand(Command):
    def __init__(self, action: Callable[[int, StoreUpdateSchema], Store], store_id: int, data: StoreUpdateSchema):
        self._action = action
        self._store_id = store_id
        self._data = data

    def execute(self) -> Store:
        return self._action(self._store_id, self._data)
