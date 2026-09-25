from datetime import date, datetime
from pydantic import BaseModel,Field
from typing import Any
from models.enums import EntityType,FilterOperator
from uuid import UUID
class Filter(BaseModel):
    field:str=Field(description=(
            "Logical field name. Use business field names only, "
            "never physical database column names. "
        ))
    operator:FilterOperator
    value:Any

class Query(BaseModel):
    entity:EntityType = Field(
        description="The business entity to search."
    )
    filters:list[Filter]|None= Field(
        default=None,
        description="Filters using logical field names."
    )

class OrderFilter(BaseModel):
    status:str|None=None
    date_from:datetime|None=None
    date_to:datetime|None=None