from ..base_service import Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, delete
from fastapi import UploadFile
from models.document import Document
from models.knowledge_base import KnowledgeBase
from models.schemas.document_schema import (GetDocument, GetAllDocument, CreateDocument,
                                            DeleteDocument, DeleteAllDocument)
from repository.rag_repo import RagRepository
from ..document_processing_service import DocumentProcessingService
from ..embedding_service import EmbeddingService


class DocumentService(Base):
    def __init__(self, db: AsyncSession):
        super().__init__()
        self.db = db
        self.processor = DocumentProcessingService()
        self.embedding_service = EmbeddingService()
        self.rag_repo = RagRepository(db=db)

    async def add_document(self, data: CreateDocument,
                           document: UploadFile) -> tuple[Document, int] | None:
        """
        the ingestion pipeline of the rag:
        file -> text -> chunks -> embeddings -> insert (document + chunks + embeddings in one transaction)
        returns None if the knowledge base does not exist
        """
        self.logger.info("starting document creation")

        try:
            knowledge_base = await self.db.get(KnowledgeBase, data.knowledge_base_id)
            if knowledge_base is None:
                return None

            text = await self.processor.extract_text(document)
            chunks = self.processor.split_text(text)
            if not chunks:
                raise ValueError("The document does not contain any text")
            self.logger.info(f"document split into {len(chunks)} chunks")

            # call the embedding api before touching the db so we don't keep a transaction open
            embeddings = await self.embedding_service.embed_documents(chunks)

            new_document = Document(knowledge_base_id=data.knowledge_base_id,
                                    filename=document.filename)
            self.db.add(new_document)
            await self.db.flush()

            chunks_count = await self.rag_repo.add_chunks(document_id=new_document.id,
                                                          chunks=chunks,
                                                          embeddings=embeddings)
            await self.db.commit()
            await self.db.refresh(new_document)

            self.logger.info("Document persisted to database successfully")
            return new_document, chunks_count

        except SQLAlchemyError:
            await self.db.rollback()
            self.logger.error("Failed to create document due to a database error", exc_info=True)
            raise

        except Exception:
            await self.db.rollback()
            self.logger.error("Failed to create document", exc_info=True)
            raise

    async def get_document_info_by_id(self, info: GetDocument) -> Document | None:
        self.logger.info("Retrieving document information")
        try:
            stmt = select(Document).where(Document.id == info.document_id,
                                          Document.knowledge_base_id == info.knowledge_base_id)
            result = await self.db.execute(stmt)
            return result.scalar_one_or_none()

        except SQLAlchemyError:
            self.logger.error("Failed to retrieve document due to a database error", exc_info=True)
            raise

        except Exception:
            self.logger.error("Failed to retrieve document", exc_info=True)
            raise

    async def get_all_document_info_by_knowledge_base_id(self, info: GetAllDocument) -> list[Document]:
        self.logger.info("Retrieving all documents of the knowledge base")
        try:
            stmt = select(Document).where(Document.knowledge_base_id == info.knowledge_base_id)
            result = await self.db.execute(stmt)
            return result.scalars().all()

        except SQLAlchemyError:
            self.logger.error("Failed to retrieve documents due to a database error", exc_info=True)
            raise

        except Exception:
            self.logger.error("Failed to retrieve documents", exc_info=True)
            raise

    async def delete_document_by_id(self, info: DeleteDocument) -> bool:
        """chunks and embeddings are removed by the ON DELETE CASCADE foreign keys"""
        self.logger.info("Deleting document by ID")
        try:
            stmt = delete(Document).where(Document.id == info.document_id,
                                          Document.knowledge_base_id == info.knowledge_base_id)
            result = await self.db.execute(stmt)
            if result.rowcount == 0:
                return False

            await self.db.commit()
            return True

        except SQLAlchemyError:
            await self.db.rollback()
            self.logger.error("Failed to delete document due to a database error", exc_info=True)
            raise

        except Exception:
            self.logger.error("Failed to delete document", exc_info=True)
            raise

    async def delete_all_document_by_knowledge_base_id(self, info: DeleteAllDocument) -> int:
        self.logger.info("Deleting all documents of the knowledge base")
        try:
            stmt = delete(Document).where(Document.knowledge_base_id == info.knowledge_base_id)
            result = await self.db.execute(stmt)
            deleted_count = result.rowcount
            if deleted_count == 0:
                return 0

            await self.db.commit()
            return deleted_count

        except SQLAlchemyError:
            await self.db.rollback()
            self.logger.error("Failed to delete documents due to a database error", exc_info=True)
            raise

        except Exception:
            self.logger.error("Failed to delete documents", exc_info=True)
            raise
