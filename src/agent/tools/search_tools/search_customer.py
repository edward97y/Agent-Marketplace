from models.schemas.query_schema import Query
from langchain_core.tools import tool
from langgraph.prebuilt import ToolRuntime
from ...context import AgentContext
@tool
async def search_customers(query:Query,runtime:ToolRuntime[AgentContext]):
    """
    Search the company's customers using filters .
    Use this tool when the customer is asking about available
    customers or wants to find a customer matching specific criteria.
    The query must contain the entity and optional filters.

    Search for customers in the company's database. This function searches the customer entity using the company's schema mapping and the filters provided in the query. Supported customer fields: - first_name: First name of the customer. - last_name: Last name or surname of the customer. - email: Email address of the customer. - phone: Phone number of the customer. - address: Physical address of the customer. - city: City where the customer is located. - country: Country where the customer is located. Important: Use the marketplace field names above, not the physical database column names. The schema mapping automatically translates marketplace fields to the company's database columns. The "name" field is not available because the company database stores first_name and last_name separately. Args:  query: Search query containing the customer entity and filters. Returns: A list of customers matching the provided filters.

    """
    company_id=runtime.state["company_id"]
    agents_runs_id=runtime.state["agent_runs_id"]
    return await runtime.context.query_service.search_for_customers(company_id=company_id,query=query,agents_runs_id=agents_runs_id)
