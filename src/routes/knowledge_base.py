from fastapi import APIRouter,status,Depends,HTTPException
from db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from services.db_services.knowledge_base_service import KnowledgeBaseService
from models.schemas.knowledge_base_schema import (CreateKnowledgeBase,GetKnowledgeBase,
                                                  GetAllKnowledgeBase,DeleteKnowledgeBase,
                                                  KnowledgeBaseResponse)

knowledge_base_router=APIRouter(prefix="/knowledge_base",tags=["knowledge_base"])

def get_knowledge_base_service(db:AsyncSession=Depends(get_db)) -> KnowledgeBaseService:
     return KnowledgeBaseService(db=db)


@knowledge_base_router.post("/create",response_model=KnowledgeBaseResponse,status_code=status.HTTP_201_CREATED)
async def create_knowledge_base(data:CreateKnowledgeBase,
                         service:KnowledgeBaseService=Depends(get_knowledge_base_service)):

    result=await service.add_knowledge_base(data=data)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="company not found"
        )
    return result


@knowledge_base_router.get("/info",response_model=KnowledgeBaseResponse,status_code=status.HTTP_200_OK)
async def get_knowledge_base_info(info:GetKnowledgeBase=Depends(),
                       service:KnowledgeBaseService=Depends(get_knowledge_base_service),):

    result=await service.get_knowledge_base_by_id(info=info)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="knowledge base not found"
        )
    return result


@knowledge_base_router.get("/info/all",response_model=list[KnowledgeBaseResponse],status_code=status.HTTP_200_OK)
async def get_all_knowledge_base_info(info:GetAllKnowledgeBase=Depends(),
                       service:KnowledgeBaseService=Depends(get_knowledge_base_service),):

    result=await service.get_all_knowledge_base_by_company_id(info=info)
    return result


@knowledge_base_router.delete("/delete",status_code=status.HTTP_204_NO_CONTENT)
async def delete_knowledge_base_by_id(info:DeleteKnowledgeBase,
                             service:KnowledgeBaseService=Depends(get_knowledge_base_service)):
 
    result=await service.delete_knowledge_base_by_id(info=info)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="knowledge base not found"
        )
