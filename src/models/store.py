class Store:
    id: int

    def __init__(self, name: str, owner_id: int, is_open: bool = False):
        self.name = name
        self.owner_id = owner_id
        self.is_open = is_open

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "owner_id": self.owner_id,
            "is_open": self.is_open,
        }

    def __repr__(self):
        return f"Store(id={self.id}, name='{self.name}', owner_id={self.owner_id}, is_open={self.is_open})"
