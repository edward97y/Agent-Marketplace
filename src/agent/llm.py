from langchain_google_genai import ChatGoogleGenerativeAI
from helpers import get_settings
from .tools.search_tools import search_products,search_orders
from .tools.action_tools import create_order

settings=get_settings()

llm=ChatGoogleGenerativeAI(api_key=settings.GEMINI_API_KEY,
                           model=settings.GEMINI_MODEL_NAME,reasoning_effort="minimal",)

tools=[search_products,search_orders,create_order]

llm_with_tools=llm.bind_tools(tools=tools)