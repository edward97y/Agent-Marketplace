from langgraph.graph.message import MessagesState
from typing import Optional
from uuid import UUID
class SalesAgentState(MessagesState):
    company_id:Optional[UUID]
    agent_runs_id:Optional[UUID]