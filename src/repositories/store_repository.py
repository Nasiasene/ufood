import sqlite3
from abc import ABC, abstractmethod
from typing import List

from models.store import Store


class StoreRepository(ABC):
    """Abstract interface for Store persistence."""

    @abstractmethod
    def add(self, store: Store) -> Store:
        ...

    @abstractmethod
    def list_stores(self) -> List[Store]:
        ...

    @abstractmethod
    def get_by_id(self, store_id: int) -> Store:
        ...

    @abstractmethod
    def update(self, store: Store) -> Store:
        ...

    @abstractmethod
    def delete(self, store_id: int) -> None:
        ...


class InMemoryStoreRepository(StoreRepository):
    def __init__(self):
        self._stores: List[Store] = []
        self._next_id = 0

    def add(self, store: Store) -> Store:
        self._next_id += 1
        store.id = self._next_id
        self._stores.append(store)
        return store

    def list_stores(self) -> List[Store]:
        return list(self._stores)

    def get_by_id(self, store_id: int) -> Store:
        for store in self._stores:
            if store.id == store_id:
                return store
        raise ValueError(f"Loja {store_id} não encontrada.")

    def update(self, store: Store) -> Store:
        for i, s in enumerate(self._stores):
            if s.id == store.id:
                self._stores[i] = store
                return store
        raise ValueError(f"Loja {store.id} não encontrada.")

    def delete(self, store_id: int) -> None:
        for i, s in enumerate(self._stores):
            if s.id == store_id:
                self._stores.pop(i)
                return
        raise ValueError(f"Loja {store_id} não encontrada.")


class SqliteStoreRepository(StoreRepository):
    def add(self, store: Store) -> Store:
        from repositories.database import get_db_connection

        try:
            with get_db_connection() as conn:
                cursor = conn.execute(
                    'INSERT INTO stores (name, owner_id, is_open) VALUES (?, ?, ?)',
                    (store.name, store.owner_id, int(store.is_open)),
                )
                if cursor.lastrowid is None:
                    raise IOError("Database did not return an ID for the inserted store")
                store.id = cursor.lastrowid
                return store
        except sqlite3.Error as e:
            raise IOError(f"Database error while adding store: {e}")

    def list_stores(self) -> List[Store]:
        from repositories.database import get_db_connection

        try:
            with get_db_connection() as conn:
                rows = conn.execute('SELECT * FROM stores').fetchall()
                return [self._row_to_store(row) for row in rows]
        except sqlite3.Error as e:
            raise IOError(f"Database error while listing stores: {e}")

    def get_by_id(self, store_id: int) -> Store:
        from repositories.database import get_db_connection

        try:
            with get_db_connection() as conn:
                row = conn.execute('SELECT * FROM stores WHERE id = ?', (store_id,)).fetchone()
                if row is None:
                    raise ValueError(f"Loja {store_id} não encontrada.")
                return self._row_to_store(row)
        except sqlite3.Error as e:
            raise IOError(f"Database error while fetching store: {e}")

    def update(self, store: Store) -> Store:
        from repositories.database import get_db_connection

        try:
            with get_db_connection() as conn:
                conn.execute(
                    'UPDATE stores SET name=?, owner_id=?, is_open=? WHERE id=?',
                    (store.name, store.owner_id, int(store.is_open), store.id),
                )
                return store
        except sqlite3.Error as e:
            raise IOError(f"Database error while updating store: {e}")

    def delete(self, store_id: int) -> None:
        from repositories.database import get_db_connection

        try:
            with get_db_connection() as conn:
                conn.execute('DELETE FROM stores WHERE id = ?', (store_id,))
        except sqlite3.Error as e:
            raise IOError(f"Database error while deleting store: {e}")

    def _row_to_store(self, row: sqlite3.Row) -> Store:
        store = Store(name=row['name'], owner_id=row['owner_id'], is_open=bool(row['is_open']))
        store.id = row['id']
        return store
