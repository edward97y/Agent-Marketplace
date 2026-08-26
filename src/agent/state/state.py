from langgraph.graph.message import MessagesState
from typing import Optional
class SalesAgentState(MessagesState):
    company_id:Optional[str]