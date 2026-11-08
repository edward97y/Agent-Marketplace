from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from models.enums.schema_enum import CompanyMappingType


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class FieldMapping(StrictModel):
    type: CompanyMappingType
    column: str | None = None
    description: str


class ProductFields(StrictModel):
    product_id: FieldMapping | None = None
    brand: FieldMapping | None = None
    name: FieldMapping | None = None
    price: FieldMapping | None = None
    color: FieldMapping | None = None
    year: FieldMapping | None = None
    size: FieldMapping | None = None
    model: FieldMapping | None = None
    in_stock: FieldMapping | None = None


class ProductMapping(StrictModel):
    table: str
    fields: ProductFields


class CustomerFields(StrictModel):
    customer_id: FieldMapping | None = None
    name: FieldMapping | None = None
    first_name: FieldMapping | None = None
    last_name: FieldMapping | None = None
    email: FieldMapping | None = None
    phone: FieldMapping | None = None
    address: FieldMapping | None = None
    city: FieldMapping | None = None
    country: FieldMapping | None = None


class CustomerMapping(StrictModel):
    table: str
    fields: CustomerFields

class OrderFields(StrictModel):
    order_id: FieldMapping | None = None
    order_number: FieldMapping | None = None
    customer_id: FieldMapping | None = None
    order_date: FieldMapping | None = None
    status: FieldMapping | None = None
    total_amount: FieldMapping | None = None


class OrderMapping(StrictModel):
    table: str
    fields: OrderFields


class OrderItemFields(StrictModel):
    order_item_id: FieldMapping | None = None
    order_id: FieldMapping | None = None
    product_id: FieldMapping | None = None
    quantity: FieldMapping | None = None
    unit_price: FieldMapping | None = None
    subtotal: FieldMapping | None = None


class OrderItemMapping(StrictModel):
    table: str
    fields: OrderItemFields


class EntityMappings(StrictModel):
    """Keys are the EntityType values. Each entity has its own model, so the
    fields of one entity can never be validated against another entity."""
    model_config = ConfigDict(extra="forbid", json_schema_extra={"example": {
        "product": {"table": "cars", "fields": {
            "product_id": {"column": "id", "type": "uuid", "description": "Unique car id"},
            "brand": {"column": "make", "type": "string", "description": "Car manufacturer"},
            "name": {"column": "model", "type": "string", "description": "Car model"},
            "price": {"column": "price", "type": "number", "description": "Selling price in USD"},
            "color": {"column": "color", "type": "string", "description": "Exterior color"},
            "year": {"column": "year", "type": "integer", "description": "Manufacturing year"},
            "in_stock": {"column": "in_stock", "type": "boolean", "description": "Available for sale"}}},
        "customer": {"table": "customers", "fields": {
            "customer_id": {"column": "id", "type": "uuid", "description": "Unique customer id"},
            "first_name": {"column": "first_name", "type": "string", "description": "First name"},
            "last_name": {"column": "last_name", "type": "string", "description": "Last name"},
            "email": {"column": "email", "type": "string", "description": "Email"}}},
        "order": {"table": "orders", "fields": {
            "order_id": {"column": "id", "type": "uuid", "description": "Unique order id"},
            "customer_id": {"column": "customer_id", "type": "uuid", "description": "Customer who ordered"},
            "order_date": {"column": "order_date", "type": "datetime", "description": "Order date"},
            "status": {"column": "status", "type": "string", "description": "pending, paid, shipped or cancelled"},
            "total_amount": {"column": "total_amount", "type": "number", "description": "Order total"}}},
        "order_items": {"table": "order_items", "fields": {
            "order_item_id": {"column": "id", "type": "uuid", "description": "Unique line id"},
            "order_id": {"column": "order_id", "type": "uuid", "description": "Order"},
            "product_id": {"column": "car_id", "type": "uuid", "description": "Car ordered"},
            "quantity": {"column": "quantity", "type": "integer", "description": "Units"},
            "unit_price": {"column": "unit_price", "type": "number", "description": "Price per unit"},
            "subtotal": {"column": "subtotal", "type": "number", "description": "quantity x unit_price"}}},
    }})

    product: ProductMapping | None = None
    order: OrderMapping | None = None
    order_items: OrderItemMapping | None = None
    customer: CustomerMapping | None = None

    def to_db(self) -> dict:
        return {
            entity: value.model_dump(mode="json")
            for entity, value in self
            if value is not None
        }


class CreateCompanyMapping(BaseModel):
    company_id: UUID
    mapping: EntityMappings


class GetCompanyMapping(BaseModel):
    """This class is for getting a specific company mapping."""

    company_id: UUID


class DeleteCompanyMapping(BaseModel):
    """This class is for deleting a specific company mapping."""

    company_id: UUID


class UpdateCompanyMapping(BaseModel):
    company_id: UUID
    mapping: EntityMappings


class CompanyMappingResponse(BaseModel):
    """Schema for company mapping API response."""

    id: UUID
    company_id: UUID
    mapping: EntityMappings
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)