from langchain_core.tools import tool
from langgraph.prebuilt import ToolRuntime

from ...context import AgentContext
from models.schemas.order_schema import CancelOrderInput


@tool
async def cancel_order(
    query: CancelOrderInput,
    runtime: ToolRuntime[AgentContext],
):
    """
    Cancel an existing order for a customer.

    Use this tool when the customer wants to cancel an existing order.

    Args:
        query: The order ID to be canceled.

    Returns:
        The canceled order information.
    """

    company_id = runtime.state["company_id"]
    agents_runs_id = runtime.state["agent_runs_id"]
    customer_id = runtime.state["customer_id"]

    return await runtime.context.order_action_service.cancel_order(
        company_id=company_id,
        agents_runs_id=agents_runs_id,
        customer_id=customer_id,
        order_id=query.order_id
    )