from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class CreateDocument(BaseModel):
    """this class for create Document post api schema """

    company_id:UUID
    file_name:str
    name:str
    document_type:str

class GetAllDocument(BaseModel):
    """this class for get all Document  schema """

    knowledge_id:UUID
    
class GetDocument(BaseModel):
    """this class for get specific Document schema """

    knowledge_id:UUID
    Document_id:UUID

class DeleteAllDocument(BaseModel):
    """this class for delete all Document  schema """

    knowledge_id:UUID
    

class DocumentResponse(BaseModel):
    """this class getting Document apis response """
    id:UUID
    knowledge_id:UUID
    filename:str
    created_at:datetime

    model_config = ConfigDict(from_attributes=True)