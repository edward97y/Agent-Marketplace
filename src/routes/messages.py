from fastapi import APIRouter,status,Depends,HTTPException,Request
from db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from services.message_service import MessageService
from models.schemas.messages_routes_schema import SendMessages,GetMessages,MessageResponse
messages_router=APIRouter(prefix="/messages",tags=["messages"])


@messages_router.post("/send/message",response_model=MessageResponse,status_code=status.HTTP_201_CREATED)
async def send_messages(data:SendMessages,request:Request,
                         db:AsyncSession=Depends(get_db),):
    agents=request.app.state.agents
    service=MessageService(db=db,conversation_id=data.conversation_id,agents=agents)
    result=await service.send_message(content=data.content)
    return result

@messages_router.get("/messages",response_model=list[MessageResponse],status_code=status.HTTP_200_OK)
async def get_messages_info(request:Request,
                            info:GetMessages=Depends(),
                            db:AsyncSession=Depends(get_db)):
    
    agents=request.app.state.agents
    service=MessageService(db=db,conversation_id=info.conversation_id,agents=agents)
    result=await service.get_messages(info=info)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="company not found"
        )
    return result


