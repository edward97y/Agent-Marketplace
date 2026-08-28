from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

from models.enums.db_enum import MessageRole


class CreateConversation(BaseModel):
    """this class for create conversation post api schema"""

    company_id: UUID
    user_id: UUID
    agent_id: UUID


class GetUserConversation(BaseModel):
    """this class for get all user conversations schema"""

    company_id: UUID


class GetAgentConversation(BaseModel):
    """this class for get all agent conversations schema"""

    company_id: UUID


class GetConversation(BaseModel):
    """this class for get specific conversation schema"""

    company_id: UUID
    agent_id: UUID


class DeleteConversation(BaseModel):
    """this class for delete all conversations schema"""
    conversation_id:UUID
    company_id: UUID


class DeleteAgent(BaseModel):
    """this class for delete specific agent conversation schema"""

    company_id: UUID
    agent_id: UUID


class GetMessages(BaseModel):
    """this class for get conversation messages schema"""

    company_id: UUID
    conversation_id: UUID


class SendMessages(BaseModel):
    """this class for send message schema"""

    company_id: UUID
    conversation_id: UUID
    content: str


class ConversationResponse(BaseModel):
    """this class for getting conversation APIs response"""

    id: UUID
    company_id: UUID
    user_id: UUID
    agent_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MessageResponse(BaseModel):
    """this class for getting message APIs response"""

    id: UUID
    conversation_id: UUID
    role: MessageRole
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)