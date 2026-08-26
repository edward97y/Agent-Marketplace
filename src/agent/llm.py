from langchain_google_genai import ChatGoogleGenerativeAI
from helpers import get_settings
from agent.tools.search_products import search_products

settings=get_settings()

llm=ChatGoogleGenerativeAI(api_key=settings.GEMINI_API_KEY,
                           model=settings.GEMINI_MODEL_NAME,temperature=0.4)

tools=[search_products]

llm_with_tools=llm.bind_tools(tools=tools)