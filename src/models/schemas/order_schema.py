from pydantic import BaseModel, Field
from uuid import UUID


class CreateOrderItemInput(BaseModel):
    product_id: UUID
    quantity: int = Field(gt=0)


class CreateOrderInput(BaseModel):
    items: list[CreateOrderItemInput] = Field(min_length=1)