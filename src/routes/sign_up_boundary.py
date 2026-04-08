from fastapi import APIRouter, HTTPException, status

from controllers.facade_singleton_controller import FacadeSingletonController
from schema.exceptions import ValidationException
from schema.user_schema import UserCreateSchema, UserResponseSchema

router = APIRouter(prefix="/usuarios", tags=["Usuários"])


class SignUpBoundary:
    def __init__(self, user_control: FacadeSingletonController):
        self._user_control = user_control
        
        router.add_api_route(
            path="/",
            endpoint=self.add_user,
            methods=["POST"],
            response_model=UserResponseSchema,
            summary="Adiciona um novo usuário",
            description="Adiciona um novo usuário ao sistema."
        )
        
    def add_user(self, user_data: UserCreateSchema):    
        try:
            
            new_user = self._user_control.sign_up(user_data)
        except ValidationException as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception:
            return {"erro": "Erro interno no servidor"}, 500
        
        return new_user.to_dict()
