from fastapi import APIRouter,status,Depends,HTTPException
from db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from services.db_services.company_service import CompanyService
from models.schemas.company_routes_schema import (AddCompany,
                                          GetCompany,DeleteCompany,CompanyResponse)

company_router=APIRouter(prefix="/company",tags=["company"])

def get_company_service(db:AsyncSession=Depends(get_db)) -> CompanyService:
     return CompanyService(db=db)


@company_router.post("/create",response_model=CompanyResponse,status_code=status.HTTP_201_CREATED)
async def create_company(data:AddCompany,
                         service:CompanyService=Depends(get_company_service)):

    result=await service.add_company(data=data)
    return result

@company_router.get("/info",response_model=CompanyResponse,status_code=status.HTTP_200_OK)
async def get_company_info(info:GetCompany=Depends(),
                       service:CompanyService=Depends(get_company_service),):
    
   

    result=await service.get_company_by_id(info=info)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="company not found"
        )
    return result


@company_router.get("/info/all",response_model=list[CompanyResponse],status_code=status.HTTP_200_OK)
async def get_all_agent_info(service:CompanyService=Depends(get_company_service),):
    
   

    result=await service.get_all_company_info()
    
    return result


@company_router.delete("/delete",status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent_by_id(info:DeleteCompany,
                             service:CompanyService=Depends(get_company_service)):
 
    result=await service.delete_company_by_id(info=info)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="company not found"
        )
    
        
