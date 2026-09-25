from langchain_core.tools import tool
from langgraph.prebuilt import ToolRuntime

from ...context import AgentContext
from models.schemas.order_schema import CreateOrderInput


@tool
async def create_order(
    query: CreateOrderInput,
    runtime: ToolRuntime[AgentContext],
):
    """
    Create a new order for a customer.

    Use this tool when the customer wants to purchase one or more
    products/cars.

    The product price is retrieved from the company's database.
    Do not provide or assume product prices from the user.

    The order total is calculated by the system based on the
    current product prices and requested quantities.

    Args:
        query: Order creation data containing 
            requested products with quantities.

    Returns:
        The created order information.
    """

    company_id = runtime.state["company_id"]
    agents_runs_id = runtime.state["agent_runs_id"]
    customer_id = runtime.state["customer_id"]

    return await runtime.context.order_action_service.create_order(
        company_id=company_id,
        agents_runs_id=agents_runs_id,
        customer_id=customer_id,
        data=query,
    )