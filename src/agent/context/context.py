from dataclasses import dataclass
from services.query_service import QueryService
@dataclass
class AgentContext:
    query_service:QueryService