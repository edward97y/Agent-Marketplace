from models.schemas.query_schema import OrderFilter
from langchain_core.tools import tool
from langgraph.prebuilt import ToolRuntime
from ...context import AgentContext
@tool
async def search_orders(query:OrderFilter,runtime:ToolRuntime[AgentContext]):
    """
    Search the company's orders using filters .
    Use this tool when the customer is asking about available
    orders or wants to find an order matching specific criteria.
    


    Search for orders in the company's database. This function searches the order entity using the company's schema mapping and the filters provided in the query. Supported order fields: - order_number: Unique order number. Currently unavailable in the company's database. - status: Current order status. Currently unavailable in the company's database. Important: Only use order fields that are marked as available in the company's schema mapping. If a requested order field is not available, do not assume or fabricate its value. Use marketplace field names, not physical database column names. Args:  query: Search query containing the order entity and filters. Returns: A list of orders matching the provided filters.

    """
    company_id=runtime.state["company_id"]
    agents_runs_id=runtime.state["agent_runs_id"]
    customer_id=runtime.state["customer_id"]
    return await runtime.context.query_service.search_for_orders(customer_id=customer_id,company_id=company_id,order_filter=query,agents_runs_id=agents_runs_id)
