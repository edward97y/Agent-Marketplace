from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

from models.enums.db_enum import MessageRole


class GetMessages(BaseModel):
    """this class for get conversation messages schema"""

    conversation_id: UUID


class SendMessages(BaseModel):
    """this class for send message schema"""

    conversation_id:UUID
    content: str

class MessageResponse(BaseModel):
    """this class for getting message APIs response"""

    id: UUID
    conversation_id: UUID
    role: MessageRole
    content: str
    

    model_config = ConfigDict(from_attributes=True)