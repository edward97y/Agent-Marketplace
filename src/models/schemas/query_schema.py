from datetime import date, datetime
from pydantic import BaseModel,Field,field_validator,model_validator
from typing import Any
from models.enums import EntityType,FilterOperator
from uuid import UUID
# small/local models often write the operator in words or symbols
OPERATOR_ALIASES = {
    "equals": "eq", "equal": "eq", "is": "eq", "==": "eq", "=": "eq",
    "not_equals": "ne", "not_equal": "ne", "!=": "ne", "<>": "ne",
    "like": "contains", "includes": "contains", "has": "contains",
    "<": "lt", "less_than": "lt", ">": "gt", "greater_than": "gt",
    "<=": "lte", "less_than_or_equal": "lte", ">=": "gte", "greater_than_or_equal": "gte",
}


class Filter(BaseModel):
    field:str=Field(description=(
            "Logical field name. Use business field names only, "
            "never physical database column names. "
        ))
    operator:FilterOperator
    value:Any


    @field_validator("operator", mode="before")
    @classmethod
    def normalize_operator(cls, value):
        if isinstance(value, str):
            key = value.strip().lower().replace(" ", "_")
            return OPERATOR_ALIASES.get(key, key)
        return value

class Query(BaseModel):
    """example: {"entity": "product", "filters": [{"field": "brand", "operator": "eq", "value": "BMW"}], "limit": 10}"""
    entity:EntityType = Field(
        description="The business entity to search."
    )
    filters:list[Filter]|None= Field(
        default=None,
        description="Filters using logical field names."
    )
    limit:int = Field(
        default=10, ge=1, le=50,
        description="Maximum number of rows to return. Keep it small (default 10)."
    )

    @model_validator(mode="before")
    @classmethod
    def accept_flat_query(cls, data):
        """small/local models sometimes send {"brand": "BMW", "in_stock": true}
        instead of entity + filters. turn the extra keys into "eq" filters."""
        if not isinstance(data, dict):
            return data
        data = dict(data)
        known = {"entity", "filters", "limit"}
        extra = {k: data.pop(k) for k in list(data) if k not in known}
        if extra:
            filters = list(data.get("filters") or [])
            filters += [{"field": k, "operator": "eq", "value": v} for k, v in extra.items()]
            data["filters"] = filters
        # this schema is only used by the product search tool
        data.setdefault("entity", "product")
        return data


class OrderFilter(BaseModel):
    status:str|None=None
    date_from:datetime|None=None
    date_to:datetime|None=None
    limit:int=Field(default=10, ge=1, le=50,
                    description="Maximum number of orders to return, newest first.")