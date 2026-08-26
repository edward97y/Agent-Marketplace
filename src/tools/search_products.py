from uuid import UUID
from models.schemas.query_schema import Query
from services.query_service import QueryService
from langchain_core.tools import tool
def create_search_products_tool(company_id:UUID, query_service:QueryService):
    @tool
    async def search_products(query:Query):
        """
        Search the company's products using filters .

        Use this tool when the customer is asking about available
        products or wants to find a product matching specific criteria.

        The query must contain the entity and optional filters.
    
        """


        return await query_service.search(company_id=company_id,query=query)
    return search_products