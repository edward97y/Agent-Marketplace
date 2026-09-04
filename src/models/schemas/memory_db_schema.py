from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime


class CreateMemory(BaseModel):
    conversation_id: UUID
    last_message_id: UUID | None = None
    summary: str


class GetMemory(BaseModel):
    
    conversation_id: UUID
   

    model_config = ConfigDict(from_attributes=True)


class UpdateMemory(BaseModel):
    conversation_id: UUID
    last_message_id: UUID
    summary: str