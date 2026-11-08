from enum import Enum

class toolTypes(str,Enum):
    SEARCH="search"
    CREATE_ORDER="create_order"
    CANCEL_ORDER="cancel_order"
    RAG="rag"
