from pydantic import BaseModel,ConfigDict
from uuid import UUID
from datetime import datetime
from models.enums.schema_enum import CompanyMappingType
from typing import Union
class FieldMapping(BaseModel):
    type: CompanyMappingType
    column: str | None=None
    description: str

class ProductFields(BaseModel):
    brand: FieldMapping | None = None
    name: FieldMapping | None = None
    price: FieldMapping | None = None
    color: FieldMapping | None = None
    year: FieldMapping | None = None
    size: FieldMapping | None = None
    model: FieldMapping | None = None
    in_stock: FieldMapping | None = None
   

class CustomerFields(BaseModel):
    first_name: FieldMapping | None = None
    last_name: FieldMapping | None = None
    name: FieldMapping | None = None
    email: FieldMapping | None = None
    phone: FieldMapping | None = None
    address: FieldMapping | None = None
    city: FieldMapping | None = None
    country: FieldMapping | None = None


class OrderFields(BaseModel):
    order_number: FieldMapping | None = None
    status: FieldMapping | None = None


class OrderMapping(BaseModel):
    table: str
    fields: OrderFields
class CustomerMapping(BaseModel):
    table: str
    fields: CustomerFields
class ProductMapping(BaseModel):
    table: str
    fields: ProductFields


class CreateCompanyMapping(BaseModel):
    company_id: UUID
    mapping: dict[str, Union[ProductMapping, CustomerMapping, OrderMapping]]

class GetCompanyMapping(BaseModel):
    """this class for get specific company mapping schema """

    company_id:UUID


class DeleteCompanyMapping(BaseModel):
    """this class for delete company mapping schema """

    company_id:UUID

class UpdateCompanyMapping(BaseModel):
    company_id:UUID
    mapping: dict[str, Union[ProductMapping, CustomerMapping, OrderMapping]]
class CompanyMappingResponse(BaseModel):
    """this class getting company apis response """
    id:UUID
    company_id: UUID
    mapping: dict[str, Union[ProductMapping, CustomerMapping, OrderMapping]]
    created_at:datetime
    updated_at:datetime
    model_config = ConfigDict(from_attributes=True)
