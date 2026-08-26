from pydantic import BaseModel
from typing import Any
from models.enums import EntityType,FilterOperator

class Filter(BaseModel):
    field:str
    operator:FilterOperator
    value:Any

class Query(BaseModel):
    entity:EntityType
    filters:list[Filter]|None=None