from fastapi import FastAPI
from routes import (agent_router,company_router,
                    company_mapping_router,user_router,
                    conversation_router,messages_router,company_config_router,
                    knowledge_base_router,document_router)
from agent.sales_agent import sales_agent
from models.enums.db_enum import AgentType
from services.company_db_maker_service import company_db_services
from db.database import engine
async def lifespan(app:FastAPI):
    app.state.agents = {
    AgentType.SALES: sales_agent,
}
    yield
    await company_db_services.close_all()
    await engine.dispose()

app=FastAPI(lifespan=lifespan)

routers=[
        agent_router,
        company_router,
        company_mapping_router,
        user_router,
        conversation_router,
        company_config_router,
        messages_router,
        knowledge_base_router,
        document_router
         ]

for router in routers:
    app.include_router(router=router)

