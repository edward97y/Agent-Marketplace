from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from models.enums.db_enum import AgentType
class CreateAgent(BaseModel):
    """this class for create agent post api schema """

    company_id:UUID
    name:str
    description:str
    type:AgentType
    is_active:bool

class GetAllAgent(BaseModel):
    """this class for get all agent  schema """

    company_id:UUID
    
class GetAgent(BaseModel):
    """this class for get specific agent schema """

    company_id:UUID
    agent_id:UUID

class DeleteAllAgent(BaseModel):
    """this class for delete all agent  schema """

    company_id:UUID
    
class DeleteAgent(BaseModel):
    """this class for delete specific agent schema """

    company_id:UUID
    agent_id:UUID


class AgentResponse(BaseModel):
    """this class getting agent apis response """
    id:UUID
    company_id:UUID
    name:str
    description:str
    type:AgentType
    is_active:bool
    created_at:datetime

    model_config = ConfigDict(from_attributes=True)