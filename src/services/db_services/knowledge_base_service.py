from ..base_service import Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, delete
from models.knowledge_base import KnowledgeBase
from models.company import Company
from models.schemas.knowledge_base_schema import (CreateKnowledgeBase, GetKnowledgeBase,
                                                  GetAllKnowledgeBase, DeleteKnowledgeBase)


class KnowledgeBaseService(Base):

    def __init__(self, db: AsyncSession):
        super().__init__()
        self.db = db

    async def add_knowledge_base(self, data: CreateKnowledgeBase) -> KnowledgeBase | None:
        """returns None if the company does not exist"""
        self.logger.info("Starting knowledge base creation")
        try:
            company = await self.db.get(Company, data.company_id)
            if company is None:
                return None

            knowledge_base = KnowledgeBase(company_id=data.company_id, name=data.name)
            self.db.add(knowledge_base)
            await self.db.commit()
            await self.db.refresh(knowledge_base)
            self.logger.info("Knowledge base persisted to database successfully")
            return knowledge_base

        except SQLAlchemyError:
            await self.db.rollback()
            self.logger.error("Failed to create knowledge base due to a database error", exc_info=True)
            raise

        except Exception:
            self.logger.error("Failed to create knowledge base", exc_info=True)
            raise

    async def get_knowledge_base_by_id(self, info: GetKnowledgeBase) -> KnowledgeBase | None:
        self.logger.info("Retrieving knowledge base information")
        try:
            stmt = select(KnowledgeBase).where(KnowledgeBase.id == info.knowledge_base_id,
                                               KnowledgeBase.company_id == info.company_id)
            result = await self.db.execute(stmt)
            return result.scalar_one_or_none()

        except SQLAlchemyError:
            self.logger.error("Failed to retrieve knowledge base due to a database error", exc_info=True)
            raise

        except Exception:
            self.logger.error("Failed to retrieve knowledge base", exc_info=True)
            raise

    async def get_all_knowledge_base_by_company_id(self, info: GetAllKnowledgeBase) -> list[KnowledgeBase]:
        self.logger.info("Retrieving all knowledge bases of the company")
        try:
            stmt = select(KnowledgeBase).where(KnowledgeBase.company_id == info.company_id)
            result = await self.db.execute(stmt)
            return result.scalars().all()

        except SQLAlchemyError:
            self.logger.error("Failed to retrieve knowledge bases due to a database error", exc_info=True)
            raise

        except Exception:
            self.logger.error("Failed to retrieve knowledge bases", exc_info=True)
            raise

    async def delete_knowledge_base_by_id(self, info: DeleteKnowledgeBase) -> bool:
        """documents, chunks and embeddings are removed by the ON DELETE CASCADE foreign keys"""
        self.logger.info("Deleting knowledge base by ID")
        try:
            stmt = delete(KnowledgeBase).where(KnowledgeBase.id == info.knowledge_base_id,
                                               KnowledgeBase.company_id == info.company_id)
            result = await self.db.execute(stmt)
            if result.rowcount == 0:
                return False

            await self.db.commit()
            return True

        except SQLAlchemyError:
            await self.db.rollback()
            self.logger.error("Failed to delete knowledge base due to a database error", exc_info=True)
            raise

        except Exception:
            self.logger.error("Failed to delete knowledge base", exc_info=True)
            raise
