
import os
import json
from typing import Dict, Any, List


class LegacyUserStorage:
    """
    Simula um sistema legado de armazenamento de usuários.
    Os métodos e estrutura de dados são diferentes do padrão atual.
    """
    FILE_PATH = 'legacy_users.json'

    def __init__(self):
        self._load()

    def _load(self):
        if os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    self._legacy_users = data.get('users', {})
                    self._next_id = data.get('next_id', 1)
                except Exception:
                    self._legacy_users = {}
                    self._next_id = 1
        else:
            self._legacy_users = {}
            self._next_id = 1

    def _save(self):
        data = {
            'next_id': self._next_id,
            'users': self._legacy_users,
        }
        with open(self.FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def save_user_legacy(self, user_dict: Dict[str, Any]) -> Dict[str, Any]:
        legacy_user = user_dict.copy()
        legacy_user['id'] = self._next_id
        self._legacy_users[str(self._next_id)] = legacy_user
        self._next_id += 1
        self._save()
        return legacy_user

    def get_user_legacy(self, user_id: int) -> Dict[str, Any]:
        key = str(user_id)
        if key not in self._legacy_users:
            raise ValueError(f"Usuário {user_id} não encontrado no sistema legado.")
        return self._legacy_users[key]

    def update_user_legacy(self, user_id: int, user_dict: Dict[str, Any]) -> Dict[str, Any]:
        key = str(user_id)
        if key not in self._legacy_users:
            raise ValueError(f"Usuário {user_id} não encontrado no sistema legado.")
        self._legacy_users[key].update(user_dict)
        self._save()
        return self._legacy_users[key]

    def get_all_users_legacy(self) -> List[Dict[str, Any]]:
        return list(self._legacy_users.values())
