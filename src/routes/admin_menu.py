from typing import List, Optional

from fastapi import APIRouter

from controllers.facade_singleton_controller import FacadeSingletonController
from filters.user_filter_strategy import (
    CompositeFilter,
    FilterByEmail,
    FilterByName,
    FilterByUserType,
    NoFilter,
)
from repositories.user_type import UserType
from schema.user_schema import UserResponseSchema

router = APIRouter(prefix="/admin", tags=["Admin"])


class AdminMenuBoundary:
    def __init__(self, user_control: FacadeSingletonController):
        self._user_control = user_control

        router.add_api_route(
            path="/",
            endpoint=self.list_users,
            methods=["GET"],
            response_model=List[UserResponseSchema],
            summary="Lista usuários",
            description="Lista usuários com filtros opcionais por nome, email e tipo.",
        )

    def list_users(
        self,
        name: Optional[str] = None,
        email: Optional[str] = None,
        user_type: Optional[str] = None,
    ):
        strategies = []
        if name:
            strategies.append(FilterByName(name))
        if email:
            strategies.append(FilterByEmail(email))
        if user_type:
            strategies.append(FilterByUserType(UserType(user_type)))

        active_filter = CompositeFilter(strategies) if strategies else NoFilter()
        return [u.to_dict() for u in self._user_control.list_users(filter=active_filter)]
        