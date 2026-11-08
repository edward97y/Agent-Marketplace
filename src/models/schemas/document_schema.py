from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class CreateDocument(BaseModel):
    """this class for create (upload) Document post api schema """

    knowledge_base_id:UUID

class GetAllDocument(BaseModel):
    """this class for get all Document  schema """

    knowledge_base_id:UUID
    
class GetDocument(BaseModel):
    """this class for get specific Document schema """

    knowledge_base_id:UUID
    document_id:UUID

class DeleteDocument(BaseModel):
    """this class for delete specific Document schema """

    knowledge_base_id:UUID
    document_id:UUID

class DeleteAllDocument(BaseModel):
    """this class for delete all Document  schema """

    knowledge_base_id:UUID
    

class DocumentResponse(BaseModel):
    """this class getting Document apis response """
    id:UUID
    knowledge_base_id:UUID
    filename:str
    created_at:datetime

    model_config = ConfigDict(from_attributes=True)

class DocumentUploadResponse(DocumentResponse):
    """this class for the upload response it also return how many chunks were embedded """
    chunks_count:int
