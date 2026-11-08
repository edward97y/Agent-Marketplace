from pydantic import BaseModel, ConfigDict, StringConstraints
from uuid import UUID
from datetime import datetime
from typing import Annotated

# the db column is String(255), validate here so a long or blank name is a 422 and not a db error
KnowledgeBaseName = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)]

class CreateKnowledgeBase(BaseModel):
    """this class for create knowledge base post api schema """

    company_id:UUID
    name:KnowledgeBaseName

class GetAllKnowledgeBase(BaseModel):
    """this class for get all knowledge bases of a company schema """

    company_id:UUID

class GetKnowledgeBase(BaseModel):
    """this class for get specific knowledge base schema """

    company_id:UUID
    knowledge_base_id:UUID

class DeleteKnowledgeBase(BaseModel):
    """this class for delete specific knowledge base schema
      (all its documents, chunks and embeddings are deleted too) """

    company_id:UUID
    knowledge_base_id:UUID

class KnowledgeBaseResponse(BaseModel):
    """this class getting knowledge base apis response """
    id:UUID
    company_id:UUID
    name:str
    created_at:datetime

    model_config = ConfigDict(from_attributes=True)
