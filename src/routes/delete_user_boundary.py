from fastapi import APIRouter, HTTPException, status

from controllers.facade_singleton_controller import FacadeSingletonController
from schema.user_schema import UserResponseSchema

router = APIRouter(prefix="/usuarios", tags=["Usuários"])


class DeleteUserBoundary:
    def __init__(self, facade: FacadeSingletonController):
        self._facade = facade

        router.add_api_route(
            path="/{user_id}",
            endpoint=self.delete_user,
            methods=["DELETE"],
            response_model=UserResponseSchema,
            summary="Exclui um usuário (soft delete)",
            description="Marca o usuário como PENDING_DELETION. Será removido definitivamente após 30 dias.",
        )

    def delete_user(self, user_id: int):
        try:
            user = self._facade.delete_user(user_id)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        return user.to_dict()
