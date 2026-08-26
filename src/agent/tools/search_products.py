from uuid import UUID
from models.schemas.query_schema import Query
from langchain_core.tools import tool
from langgraph.prebuilt import ToolRuntime
from ..context import SalesAgentContext
@tool
async def search_products(query:Query,runtime:ToolRuntime[SalesAgentContext]):
    """
    Search the company's products using filters .
    Use this tool when the customer is asking about available
    products or wants to find a product matching specific criteria.
    The query must contain the entity and optional filters.

    """
    company_id=runtime.state["company_id"]

    return await runtime.context.query_service.search(company_id=company_id,query=query)
