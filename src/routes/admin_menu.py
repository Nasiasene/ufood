from fastapi import APIRouter
from typing import List

from controllers.user_control import UserControl
from schema.user_schema import UserResponseSchema


router = APIRouter(prefix="/admin", tags=["Admin"])

class AdminMenuBoundary:
    def __init__(self, user_control: UserControl):
        self._user_control = user_control
        
        router.add_api_route(
            path="/",
            endpoint=self.list_users,
            methods=["GET"],
            response_model=List[UserResponseSchema],
            summary="Lista usuários",
            description="Lista usuários"
        )

    def list_users(self):
        return [user.to_dict() for user in self._user_control.list_users()]
        