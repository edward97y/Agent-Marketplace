from langchain_core.tools import tool
from langgraph.prebuilt import ToolRuntime

from ...context import AgentContext
from models.schemas.rag_schema import RagQuery


@tool
async def rag_search(
    query: RagQuery,
    runtime: ToolRuntime[AgentContext],
):
    """
    Search the company's knowledge base (uploaded documents such as policies,
    FAQs, warranty, shipping, return and payment information, guides and manuals).

    Use this tool when the customer asks a general question about the company,
    its services or its policies that is NOT about live product data
    (price, stock, color...) and NOT about the customer's own orders.
    For products use `search_products`, for orders use `search_orders`.

    The search is hybrid: it combines semantic (meaning) search and keyword
    search, so include the important keywords, names and numbers from the
    customer's question.

    Args:
        query: A self-contained question and optional number of passages.

    Returns:
        A list of passages ordered by relevance. Each passage has the source
        filename and its content. Answer ONLY from these passages. If the list is
        empty or the passages do not answer the question, say that the information
        is not available.
    """

    company_id = runtime.state["company_id"]
    agents_runs_id = runtime.state["agent_runs_id"]

    return await runtime.context.rag_service.hybrid_search(
        company_id=company_id,
        agents_runs_id=agents_runs_id,
        query=query,
    )
