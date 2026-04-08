from typing import Optional

from pydantic import BaseModel, Field


class StoreCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    owner_id: int
    is_open: bool = False


class StoreUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    is_open: Optional[bool] = None


class StoreResponseSchema(BaseModel):
    id: int
    name: str
    owner_id: int
    is_open: bool
