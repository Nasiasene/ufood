from typing import List

from repositories.user_repository import UserRepository, User
from schema.user_schema import UserCreateSchema
from repositories.user_type import UserType

class UserControl:
    def __init__(self, repository: UserRepository):
        self._repository = repository
        
    def sign_up(self, user_data: UserCreateSchema):
        user_type = UserType.USER if user_data.user_type.value == "user" else UserType.ADMIN
        
        new_user = User(
            name=user_data.name,
            email=user_data.email,
            user_type=user_data.user_type,
            phone=user_data.phone
        )
        
        return self._repository.add(new_user)
    
    def list_users(self) -> List[User]:
        return self._repository.list_users()
        
        