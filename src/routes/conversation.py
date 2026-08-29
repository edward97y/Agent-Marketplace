from fastapi import APIRouter,status,Depends,HTTPException
from models.schemas.conversation_routes_schema import (CreateConversation,GetAgentConversation,
                                               GetConversation,GetUserConversation,ConversationResponse,
                                               DeleteAgentConversation,DeleteConversation)
from db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from services.db_services.conversation_service import ConversationService

def get_conversation_service(db:AsyncSession=Depends(get_db)) -> ConversationService:
     return ConversationService(db=db)
conversation_router=APIRouter(prefix="/conversation", tags=["conversation"])

@conversation_router.post("/create",response_model=ConversationResponse,status_code=status.HTTP_201_CREATED)
async def create_conversation(conversation_data:CreateConversation,
                       service:ConversationService=Depends(get_conversation_service),):


    result=await service.add_conversation(data=conversation_data)

    return result


@conversation_router.get("/info",response_model=ConversationResponse,status_code=status.HTTP_200_OK)
async def get_conversation_info(info:GetConversation=Depends(),
                       service:ConversationService=Depends(get_conversation_service),):
    
   

    result=await service.get_conversation_info_by_id(info=info)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="conversation not found"
        )
    return result

@conversation_router.get("/info/user",response_model=ConversationResponse,status_code=status.HTTP_200_OK)
async def get_user_conversation_info(info:GetUserConversation=Depends(),
                       service:ConversationService=Depends(get_conversation_service),):
    
   

    result=await service.get_user_conversations(info=info)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="conversation not found"
        )
    return result

@conversation_router.get("/info/agent",response_model=ConversationResponse,status_code=status.HTTP_200_OK)
async def get_agent_conversation_info(info:GetAgentConversation=Depends(),
                       service:ConversationService=Depends(get_conversation_service),):
    
   

    result=await service.get_agent_conversations(info=info)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="conversation not found"
        )
    return result



@conversation_router.delete("/delete",status_code=status.HTTP_204_NO_CONTENT)

async def delete_conversation_by_id(info:DeleteConversation,
                             service:ConversationService=Depends(get_conversation_service)):
 
    result=await service.delete_conversation_by_id(info=info)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="conversation not found"
        )
    
        


@conversation_router.delete("/delete/agent",status_code=status.HTTP_200_OK)

async def delete_all_conversation_by_company_id(info:DeleteAgentConversation,
                                         service:ConversationService=Depends(get_conversation_service),):

    
        result=await service.delete_agent_conversation_by_id(info=info)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="conversation not found"
            )
        return {
        "message": "conversations deleted successfully",
        "deleted_count": result
    }
        



