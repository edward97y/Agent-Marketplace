from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from models.enums.db_enum import DatabaseType

class AddCompanyDBConfig(BaseModel):
    """this class for add company post api schema """
    company_id:UUID
    host:str
    name:str
    username:str
    password:str
    port:int
    type:DatabaseType
   

    
class GetCompanyDBConfig(BaseModel):
    """this class for get specific company schema """
    
    company_id:UUID


class DeleteCompanyDBConfig(BaseModel):
    """this class for delete company  schema """

    company_id:UUID
    company_db_id:UUID


class CompanyResponse(BaseModel):
    """this class getting company apis response """
    id:UUID
    company_id:UUID
    host:str
    name:str
    username:str
    password:str
    port:int
    type:DatabaseType
    created_at:datetime

    model_config = ConfigDict(from_attributes=True)