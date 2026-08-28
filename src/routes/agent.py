from fastapi import APIRouter,status,Depends,HTTPException
from models.schemas.agent_routes_schema import (CreateAgent,GetAllAgent,
                                          GetAgent,AgentResponse,
                                          DeleteAllAgent,DeleteAgent)
from db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from services.db_services.agent_service import AgentService

def get_agent_service(db:AsyncSession=Depends(get_db)) -> AgentService:
     return AgentService(db=db)
agent_router=APIRouter(prefix="/agent", tags=["agent"])

@agent_router.post("/create",response_model=AgentResponse,status_code=status.HTTP_201_CREATED)
async def create_agent(agent_data:CreateAgent,
                       service:AgentService=Depends(get_agent_service),):


    result=await service.create_agent(data=agent_data)

    return result


@agent_router.get("/info",response_model=AgentResponse,status_code=status.HTTP_200_OK)
async def get_agent_info(info:GetAgent=Depends(),
                       service:AgentService=Depends(get_agent_service),):
    
   

    result=await service.get_agent_info_by_id(info=info)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Agent not found"
        )
    return result


@agent_router.get("/info/all",response_model=list[AgentResponse],status_code=status.HTTP_200_OK)
async def get_all_agent_info(info:GetAllAgent=Depends(),
                       service:AgentService=Depends(get_agent_service)):
    
   

    result=await service.get_all_agent_info_by_company_id(info=info)
    
    return result



@agent_router.delete("/delete",status_code=status.HTTP_204_NO_CONTENT)

async def delete_agent_by_id(info:DeleteAgent,
                             service:AgentService=Depends(get_agent_service)):
 
    result=await service.delete_agent_by_id(info=info)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
        


@agent_router.delete("/delete/all",status_code=status.HTTP_200_OK)

async def delete_all_agent_by_company_id(info:DeleteAllAgent,
                                         service:AgentService=Depends(get_agent_service),):

    
        result=await service.delete_all_agent_by_company_id(info=info)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent not found"
            )
        return {
        "message": "Agents deleted successfully",
        "deleted_count": result
    }
        



