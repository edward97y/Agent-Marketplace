from pydantic import BaseModel
from typing import Any,Optional
from models.enums import EntityType

class Filter(BaseModel):
    field:str
    operator:str
    value:Any

class Query(BaseModel):
    entity:EntityType
    filters:Optional[Filter]|None=None