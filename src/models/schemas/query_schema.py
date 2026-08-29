from pydantic import BaseModel,Field
from typing import Any
from models.enums import EntityType,FilterOperator

class Filter(BaseModel):
    field:str=Field(description=(
            "Logical field name. Use business field names only, "
            "never physical database column names. "
            "For example, use 'brand', not 'make'."
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