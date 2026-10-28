from ..base_service import Base
from sqlalchemy.ext.asyncio import AsyncSession
from models.schemas.document_schema import (GetDocument,GetAllDocument,
                                            DocumentResponse,CreateDocument)
from fastapi import UploadFile
from models.document import Document
class DocumentService(Base):
    def __init__(self, db:AsyncSession):
        super().__init__()
        self.db=db
    async def add_document(self,data:CreateDocument,document:UploadFile)->Document:
        self.logger.info("starting document creation")
        new_document=Document(company_id=data.company_id,document_name=data.document_name,
                              document_type=data.document_type,document_file=document.file.read())