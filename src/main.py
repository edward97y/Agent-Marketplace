from fastapi import FastAPI
from helpers.config import get_settings
from routes import agent_router,company_router,company_mapping_router

async def lifespan(app:FastAPI):
    settings=get_settings()
    yield
    pass

app=FastAPI(lifespan=lifespan)

routers=[agent_router,
         company_router,
         company_mapping_router
         ]

for router in routers:
    app.include_router(router=router)