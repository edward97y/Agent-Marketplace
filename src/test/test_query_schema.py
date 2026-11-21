import pytest
from pydantic import ValidationError

from models.enums import EntityType, FilterOperator
from models.schemas.query_schema import Filter, Query


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("eq", FilterOperator.EQ),
        ("equals", FilterOperator.EQ),
        ("==", FilterOperator.EQ),
        ("!=", FilterOperator.NE),
        ("like", FilterOperator.CONTAINS),
        ("<", FilterOperator.LT),
        (">=", FilterOperator.GTE),
        ("  Less Than  ", FilterOperator.LT),
    ],
)
def test_filter_normalizes_operator_aliases(raw, expected):
    f = Filter(field="price", operator=raw, value=30000)
    assert f.operator == expected


def test_filter_rejects_unknown_operator():
    with pytest.raises(ValidationError):
        Filter(field="price", operator="between", value=1)


def test_query_defaults():
    q = Query(entity="order")
    assert q.entity == EntityType.ORDER
    assert q.filters is None
    assert q.limit == 10


def test_query_defaults_entity_to_product():
    q = Query.model_validate({"filters": []})
    assert q.entity == EntityType.PRODUCT


def test_query_flat_keys_become_eq_filters():
    q = Query.model_validate({"brand": "BMW", "in_stock": True})
    assert q.entity == EntityType.PRODUCT
    assert [(f.field, f.operator, f.value) for f in q.filters] == [
        ("brand", FilterOperator.EQ, "BMW"),
        ("in_stock", FilterOperator.EQ, True),
    ]


def test_query_flat_keys_are_appended_to_existing_filters():
    q = Query.model_validate(
        {
            "filters": [{"field": "price", "operator": "<", "value": 30000}],
            "brand": "BMW",
        }
    )
    assert [(f.field, f.operator) for f in q.filters] == [
        ("price", FilterOperator.LT),
        ("brand", FilterOperator.EQ),
    ]


@pytest.mark.parametrize("limit", [0, 51])
def test_query_limit_out_of_range_is_rejected(limit):
    with pytest.raises(ValidationError):
        Query(entity="product", limit=limit)
