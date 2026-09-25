from enum import Enum

class EntityType(str,Enum):
    PRODUCT="product"
    ORDER="order"
    ORDER_ITEMS="order_items"
    CUSTOMER="customer"