from fastapi import APIRouter, HTTPException, status

from controllers.facade_singleton_controller import FacadeSingletonController
from schema.exceptions import ValidationException
from schema.user_schema import UserResponseSchema, UserUpdateSchema

router = APIRouter(prefix="/usuarios", tags=["Usuários"])


class EditUserBoundary:
    def __init__(self, facade: FacadeSingletonController):
        self._facade = facade

        router.add_api_route(
            path="/{user_id}",
            endpoint=self.edit_user,
            methods=["PUT"],
            response_model=UserResponseSchema,
            summary="Edita um usuário",
            description="Atualiza os campos de um usuário existente. Salva snapshot para permitir desfazer.",
        )
        router.add_api_route(
            path="/{user_id}/undo",
            endpoint=self.undo_edit,
            methods=["POST"],
            response_model=UserResponseSchema,
            summary="Desfaz última edição",
            description="Restaura o estado anterior do usuário (Memento).",
        )

    def edit_user(self, user_id: int, user_data: UserUpdateSchema):
        try:
            user = self._facade.edit_user(user_id, user_data)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except ValidationException as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        return user.to_dict()

    def undo_edit(self, user_id: int):
        try:
            user = self._facade.undo_last_edit(user_id)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        return user.to_dict()
