from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from helpers import get_settings
from .tools.search_tools import search_products,search_orders
from .tools.action_tools import create_order,cancel_order
from .tools.rag_tools import rag_search

settings=get_settings()

tools=[search_products,search_orders,create_order,cancel_order,rag_search]

# main model: Gemini
gemini_llm=ChatGoogleGenerativeAI(api_key=settings.GEMINI_API_KEY,
                                  model=settings.GEMINI_MODEL_NAME,reasoning_effort="minimal",
                                  max_retries=settings.GEMINI_MAX_RETRIES,
                                  timeout=settings.GEMINI_TIMEOUT_SECONDS)


local_llm=ChatOllama(model=settings.LOCAL_LLM_MODEL_NAME,
                     base_url=settings.OLLAMA_BASE_URL,
                     num_ctx=settings.LOCAL_LLM_NUM_CTX,
                     reasoning=False,  
                     temperature=0.3,
                     keep_alive="30m",
                     client_kwargs={"timeout":settings.LOCAL_LLM_TIMEOUT_SECONDS})

if settings.LOCAL_LLM_ENABLED:
    llm=gemini_llm.with_fallbacks([local_llm])
    llm_with_tools=gemini_llm.bind_tools(tools=tools).with_fallbacks([local_llm.bind_tools(tools=tools)])
else:
    llm=gemini_llm
    llm_with_tools=gemini_llm.bind_tools(tools=tools)
