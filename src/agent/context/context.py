from dataclasses import dataclass
from services.query_service import QueryService
from services.actions_service import OrderActionService
@dataclass
class AgentContext:
    query_service:QueryService
    order_action_service:OrderActionService