from langgraph.graph.message import MessagesState
from uuid import UUID
class SalesAgentState(MessagesState):
    summary:str | None = None
    company_id:UUID
    agent_runs_id:UUID