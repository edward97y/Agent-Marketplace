from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime



class CreateConversation(BaseModel):
    """this class for create conversation post api schema"""

    company_id: UUID
    user_id: UUID
    agent_id: UUID


class GetUserConversation(BaseModel):
    """this class for get all user conversations schema"""

    company_id: UUID
    user_id:UUID


class GetAgentConversation(BaseModel):
    """this class for get all agent conversations schema"""

    company_id: UUID
    agent_id:UUID


class GetConversation(BaseModel):
    """this class for get specific conversation schema"""
    
    conversation_id:UUID


class DeleteConversation(BaseModel):
    """this class for delete all conversations schema"""
    conversation_id:UUID
    company_id: UUID


class DeleteAgentConversation(BaseModel):
    """this class for delete specific agent conversation schema"""

    company_id: UUID
    agent_id: UUID

class ConversationResponse(BaseModel):
    """this class for getting conversation APIs response"""

    id: UUID
    company_id: UUID
    user_id: UUID
    agent_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

