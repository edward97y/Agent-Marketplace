from fastapi import APIRouter,status,Depends,HTTPException
from db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from services.db_services.company_db_config_service import CompanyDBService
from models.schemas.company_db_config_routes_schema import (AddCompanyDBConfig,GetCompanyDBConfig,
                                                            DeleteCompanyDBConfig,CompanyResponse)

company_config_router=APIRouter(prefix="/company_config",tags=["company_config"])

def get_company_config_service(db:AsyncSession=Depends(get_db)) -> CompanyDBService:
     return CompanyDBService(db=db)


@company_config_router.post("/create",response_model=CompanyResponse,status_code=status.HTTP_201_CREATED)
async def create_company(data:AddCompanyDBConfig,
                         service:CompanyDBService=Depends(get_company_config_service)):

    result=await service.add_company(data=data)
    return result

@company_config_router.get("/info",response_model=CompanyResponse,status_code=status.HTTP_200_OK)
async def get_company_info(info:GetCompanyDBConfig=Depends(),
                       service:CompanyDBService=Depends(get_company_config_service),):
    
   

    result=await service.get_company_by_id(info=info)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="company not found"
        )
    return result



@company_config_router.delete("/delete",status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent_by_id(info:DeleteCompanyDBConfig,
                             service:CompanyDBService=Depends(get_company_config_service)):
 
    result=await service.delete_company_by_id(info=info)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="company not found"
        )
    
        
