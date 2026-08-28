from pydantic import BaseModel, ConfigDict,EmailStr
from uuid import UUID
from datetime import datetime
from models.enums.db_enum import UserRole

class AddUser(BaseModel):
    """this class for add user"""
    company_id:UUID
    email:EmailStr
    password:str
    role:UserRole
   

    
class GetUser(BaseModel):
    """this class for get  users """

    user_id:UUID
    company_id:UUID

class GetAllUser(BaseModel):
    """this class for get all users for specific company"""
    company_id:UUID

class DeleteUser(BaseModel):
    """this class for delete user from company schema """

    company_id:UUID
    user_id:UUID

class UserResponse(BaseModel):
    """this class getting user apis response """
    id:UUID
    company_id:UUID
    email:str
    password_hash:str
    role:UserRole
    created_at:datetime

    model_config = ConfigDict(from_attributes=True)