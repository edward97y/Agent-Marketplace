from fastapi import APIRouter,status,Depends,HTTPException,UploadFile,File
from models.schemas.document_schema import (GetDocument,GetAllDocument,DocumentResponse,CreateDocument,
                                            DeleteDocument,DeleteAllDocument,DocumentUploadResponse)
from db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from services.db_services.document_service import DocumentService

document_router=APIRouter(prefix="/document", tags=["document"])


def get_document_service(db:AsyncSession=Depends(get_db)) -> DocumentService:
     return DocumentService(db=db)


@document_router.post("/create",response_model=DocumentUploadResponse,status_code=status.HTTP_201_CREATED)
async def create_document(document:UploadFile=File(...),data:CreateDocument=Depends(),
                          service:DocumentService=Depends(get_document_service),):
    """upload a file (.txt .md .csv .json .pdf) -> it is chunked, embedded and stored for the rag tool"""

    try:
        result=await service.add_document(data=data,document=document)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="knowledge base not found"
        )

    new_document,chunks_count=result
    return DocumentUploadResponse(
        **DocumentResponse.model_validate(new_document).model_dump(),
        chunks_count=chunks_count
    )


@document_router.get("/info",response_model=DocumentResponse,status_code=status.HTTP_200_OK)
async def get_document_info(info:GetDocument=Depends(),
                       service:DocumentService=Depends(get_document_service),):

    result=await service.get_document_info_by_id(info=info)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="document not found"
        )
    return result


@document_router.get("/info/all",response_model=list[DocumentResponse],status_code=status.HTTP_200_OK)
async def get_all_document_info(info:GetAllDocument=Depends(),
                       service:DocumentService=Depends(get_document_service)):

    result=await service.get_all_document_info_by_knowledge_base_id(info=info)
    return result


@document_router.delete("/delete",status_code=status.HTTP_204_NO_CONTENT)
async def delete_document_by_id(info:DeleteDocument,
                             service:DocumentService=Depends(get_document_service)):
 
    result=await service.delete_document_by_id(info=info)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="document not found"
        )


@document_router.delete("/delete/all",status_code=status.HTTP_200_OK)
async def delete_all_document_by_knowledge_base_id(info:DeleteAllDocument,
                                         service:DocumentService=Depends(get_document_service),):

    result=await service.delete_all_document_by_knowledge_base_id(info=info)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="document not found"
        )
    return {
        "message": "documents deleted successfully",
        "deleted_count": result
    }
