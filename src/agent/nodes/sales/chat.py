from ...llm import llm_with_tools
from ...state import SalesAgentState
from langchain.messages import SystemMessage
from ...prompt.sales_prompt import SYSTEM_PROMPT
async def chat_node(state:SalesAgentState):
    """
    this is the brain of the sales agent it use to answer the user question
    or to call tools
    """
    messages=[
        SystemMessage(content=SYSTEM_PROMPT),
        *state['messages'],
    ]

    response=llm_with_tools.invoke(messages)
    return{
        "messages":[response]
    }
