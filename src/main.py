from fastapi import FastAPI
from helpers.config import get_settings
from routes import (agent_router,company_router,
                    company_mapping_router,user_router,
                    conversation_router,messages_router,company_config_router)
from agent.sales_agent import sales_agent
from models.enums.db_enum import AgentType
async def lifespan(app:FastAPI):
    settings=get_settings()
    app.state.agents = {
    AgentType.SALES: sales_agent,
}
    yield
    pass

app=FastAPI(lifespan=lifespan)

routers=[
        agent_router,
        company_router,
        company_mapping_router,
        user_router,
        conversation_router,
        company_config_router,
        messages_router
         ]

for router in routers:
    app.include_router(router=router)