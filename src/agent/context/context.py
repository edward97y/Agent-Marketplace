from dataclasses import dataclass
from services.query_service import QueryService
from services.actions_service import OrderActionService
from services.rag_service import RagService
@dataclass
class AgentContext:
    query_service:QueryService
    order_action_service:OrderActionService
    rag_service:RagService
