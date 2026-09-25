from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from models.enums.schema_enum import CompanyMappingType
from typing import Union


class FieldMapping(BaseModel):
    type: CompanyMappingType
    column: str | None = None
    description: str


class ProductFields(BaseModel):
    product_id: FieldMapping | None = None
    brand: FieldMapping | None = None
    name: FieldMapping | None = None
    price: FieldMapping | None = None
    color: FieldMapping | None = None
    year: FieldMapping | None = None
    size: FieldMapping | None = None
    model: FieldMapping | None = None
    in_stock: FieldMapping | None = None


class ProductMapping(BaseModel):
    table: str
    fields: ProductFields


class CustomerFields(BaseModel):
    customer_id: FieldMapping | None = None
    name: FieldMapping | None = None
    first_name: FieldMapping | None = None
    last_name: FieldMapping | None = None
    email: FieldMapping | None = None
    phone: FieldMapping | None = None
    address: FieldMapping | None = None
    city: FieldMapping | None = None
    country: FieldMapping | None = None


class CustomerMapping(BaseModel):
    table: str
    fields: CustomerFields

class OrderFields(BaseModel):
    order_id: FieldMapping | None = None
    order_number: FieldMapping | None = None
    customer_id: FieldMapping | None = None
    order_date: FieldMapping | None = None
    status: FieldMapping | None = None
    total_amount: FieldMapping | None = None


class OrderMapping(BaseModel):
    table: str
    fields: OrderFields


class OrderItemFields(BaseModel):
    order_item_id: FieldMapping | None = None
    order_id: FieldMapping | None = None
    product_id: FieldMapping | None = None
    quantity: FieldMapping | None = None
    unit_price: FieldMapping | None = None
    subtotal: FieldMapping | None = None


class OrderItemMapping(BaseModel):
    table: str
    fields: OrderItemFields


class CreateCompanyMapping(BaseModel):
    company_id: UUID
    mapping: dict[
        str,
        Union[
            ProductMapping,
            OrderMapping,
            OrderItemMapping,
            CustomerMapping,
        ]
    ]


class GetCompanyMapping(BaseModel):
    """This class is for getting a specific company mapping."""

    company_id: UUID


class DeleteCompanyMapping(BaseModel):
    """This class is for deleting a specific company mapping."""

    company_id: UUID


class UpdateCompanyMapping(BaseModel):
    company_id: UUID
    mapping: dict[
        str,
        Union[
            ProductMapping,
            OrderMapping,
            OrderItemMapping,
            CustomerMapping,
        ]
    ]


class CompanyMappingResponse(BaseModel):
    """Schema for company mapping API response."""

    id: UUID
    company_id: UUID
    mapping: dict[
        str,
        Union[
            ProductMapping,
            OrderMapping,
            OrderItemMapping,
            CustomerMapping,
        ]
    ]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)