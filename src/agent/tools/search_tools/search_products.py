from models.schemas.query_schema import Query
from langchain_core.tools import tool
from langgraph.prebuilt import ToolRuntime
from ...context import AgentContext
@tool
async def search_products(query:Query,runtime:ToolRuntime[AgentContext]):
    """
    Search the company's products using filters .
    Use this tool when the customer is asking about available
    products or wants to find a product matching specific criteria.
    The query must contain the entity and optional filters.

    Search for products available in the company's database. This function searches the product entity using the company's schema mapping and the filters provided in the query. Supported product fields: - brand: Car manufacturer or brand, e.g. BMW, Toyota, Mercedes.
      - name: Specific vehicle model or product name. - price: Selling price of the vehicle. - color: Exterior color of the vehicle. - year: Manufacturing year. - in_stock: Whether the vehicle is currently available for sale. Important: Use the marketplace field names above,
        not the physical database column names. The schema mapping automatically translates marketplace fields to the company's database columns. 
        query: Search query containing the product entity and filters. Returns: A list of products matching the provided filters. """


    company_id=runtime.state["company_id"]
    agents_runs_id=runtime.state["agent_runs_id"]
    return await runtime.context.query_service.search_for_products(company_id=company_id,query=query,agents_runs_id=agents_runs_id)
