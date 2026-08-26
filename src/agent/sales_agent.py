from langgraph.graph import StateGraph, START
from langgraph.prebuilt import tools_condition,ToolNode
from .state import SalesAgentState
from .llm import tools
from .nodes.sales.chat import chat_node
from .context import SalesAgentContext

graph=StateGraph(SalesAgentState,context_schema=SalesAgentContext)

graph.add_node("chat",chat_node)
graph.add_node("tools",ToolNode(tools))

graph.add_edge(START,"chat")
graph.add_conditional_edges("chat",tools_condition)
graph.add_edge("tools","chat")


sales_agent=graph.compile()