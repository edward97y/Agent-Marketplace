from fastapi import APIRouter,status,Depends,HTTPException
from db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from services.db_services.company_mapping_service import CompanyMappingService
from models.schemas.company_mapping_schema import (CreateCompanyMapping,
                                                   GetCompanyMapping,
                                                   DeleteCompanyMapping,CompanyMappingResponse)
company_mapping_router=APIRouter(prefix="/company_mapping",tags=["company_mapping"])

def get_company_mapping_service(db:AsyncSession=Depends(get_db)) -> CompanyMappingService:
     return CompanyMappingService(db=db)


@company_mapping_router.post("/create",response_model=CompanyMappingResponse,status_code=status.HTTP_201_CREATED)
async def create_company(data:CreateCompanyMapping,
                         service:CompanyMappingService=Depends(get_company_mapping_service)):

    result=await service.add_company_mapping(data=data)
    return result

@company_mapping_router.get("/info",response_model=CompanyMappingResponse,status_code=status.HTTP_200_OK)
async def get_company_info(info:GetCompanyMapping=Depends(),
                       service:CompanyMappingService=Depends(get_company_mapping_service),):
    
   

    result=await service.get_company_mapping_by_id(info=info)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="company not found"
        )
    return result



@company_mapping_router.delete("/delete",status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent_by_id(info:DeleteCompanyMapping,
                             service:CompanyMappingService=Depends(get_company_mapping_service)):
 
    result=await service.delete_company_mapping_by_id(info=info)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="company not found"
        )
    
        
