from fastapi import APIRouter,status,Depends,HTTPException

from models.schemas.user_routes_schema import (AddUser,GetAllUser
                                               ,GetUser,DeleteUser,UserResponse)
from db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from services.db_services.user_service import UserService

def get_user_service(db:AsyncSession=Depends(get_db)) -> UserService:
     return UserService(db=db)
user_router=APIRouter(prefix="/user", tags=["user"])

@user_router.post("/create",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
async def create_user(user_data:AddUser,
                       service:UserService=Depends(get_user_service),):


    result=await service.create_user(data=user_data)

    return result


@user_router.get("/info",response_model=UserResponse,status_code=status.HTTP_200_OK)
async def get_user_info(info:GetUser=Depends(),
                       service:UserService=Depends(get_user_service),):
    
   

    result=await service.get_user_info_by_id(info=info)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="user not found"
        )
    return result


@user_router.get("/info/all",response_model=list[UserResponse],status_code=status.HTTP_200_OK)
async def get_all_user_info(info:GetAllUser=Depends(),
                       service:UserService=Depends(get_user_service)):
    
   

    result=await service.get_all_user_info_by_company_id(info=info)
    
    return result



@user_router.delete("/delete",status_code=status.HTTP_204_NO_CONTENT)

async def delete_user_by_id(info:DeleteUser,
                             service:UserService=Depends(get_user_service)):
 
    result=await service.delete_user_by_id(info=info)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )
    
        

