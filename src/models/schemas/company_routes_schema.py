from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from models.enums.db_enum import PlanType
class AddCompany(BaseModel):
    """this class for add company post api schema """
    name:str
    plan:PlanType
   

    
class GetCompany(BaseModel):
    """this class for get specific company schema """

    company_id:UUID


class DeleteCompany(BaseModel):
    """this class for delete company  schema """

    company_id:UUID


class CompanyResponse(BaseModel):
    """this class getting company apis response """
    id:UUID
    name:str
    plan:PlanType
    created_at:datetime

    model_config = ConfigDict(from_attributes=True)