from typing import List

from fastapi import APIRouter, HTTPException, status

from controllers.facade_singleton_controller import FacadeSingletonController
from schema.store_schema import StoreCreateSchema, StoreResponseSchema, StoreUpdateSchema

router = APIRouter(prefix="/lojas", tags=["Lojas"])


class StoresBoundary:
    def __init__(self, facade: FacadeSingletonController):
        self._facade = facade

        router.add_api_route("/", self.create_store, methods=["POST"], response_model=StoreResponseSchema, summary="Cadastra uma loja")
        router.add_api_route("/", self.list_stores, methods=["GET"], response_model=List[StoreResponseSchema], summary="Lista lojas")
        router.add_api_route("/{store_id}", self.edit_store, methods=["PUT"], response_model=StoreResponseSchema, summary="Edita uma loja")
        router.add_api_route("/{store_id}", self.delete_store, methods=["DELETE"], summary="Exclui uma loja")
        router.add_api_route("/count", self.count_entities, methods=["GET"], summary="Conta total de entidades")

    def create_store(self, data: StoreCreateSchema):
        try:
            return self._facade.create_store(data).to_dict()
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    def list_stores(self):
        return [s.to_dict() for s in self._facade.list_stores()]

    def edit_store(self, store_id: int, data: StoreUpdateSchema):
        try:
            return self._facade.edit_store(store_id, data).to_dict()
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    def delete_store(self, store_id: int):
        try:
            self._facade.delete_store(store_id)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        return {"message": f"Loja {store_id} removida com sucesso."}

    def count_entities(self):
        return {"total_entities": self._facade.count_entities()}
