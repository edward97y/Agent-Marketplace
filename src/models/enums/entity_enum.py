from enum import Enum

class EntityType(str,Enum):
    PRODUCT="product"
    CUSTOMER="customer"
    ORDER="order"
    APPOINTMENT="appointment"

