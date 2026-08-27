from pydantic import BaseModel,ConfigDict
from uuid import UUID
from datetime import datetime
from models.enums.schema_enum import CompanyMappingType
class FieldMapping(BaseModel):
    type: CompanyMappingType
    column: str
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
   


class ProductMapping(BaseModel):
    table: str
    fields: ProductFields


class CreateCompanyMapping(BaseModel):
    company_id: UUID
    mapping: dict[str, ProductMapping]

class GetCompanyMapping(BaseModel):
    """this class for get specific company mapping schema """

    company_id:UUID


class DeleteCompanyMapping(BaseModel):
    """this class for delete company mapping schema """

    company_id:UUID


class CompanyMappingResponse(BaseModel):
    """this class getting company apis response """
    id:UUID
    company_id: UUID
    mapping: dict[str, ProductMapping]
    created_at:datetime
    updated_at:datetime
    model_config = ConfigDict(from_attributes=True)
