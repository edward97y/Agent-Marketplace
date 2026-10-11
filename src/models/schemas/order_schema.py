from pydantic import BaseModel, Field
from uuid import UUID


class CreateOrderItemInput(BaseModel):
    product_id: UUID
    quantity: int = Field(gt=0)


class CreateOrderInput(BaseModel):
    items: list[CreateOrderItemInput] = Field(min_length=1)

class CancelOrderInput(BaseModel):
    order_id: UUID=Field(description="The unique identifier of the order to be canceled. u need to search for the user orders and let him choose what the order that he want to cancel if there is only one order there is no need to ask just get the order id")