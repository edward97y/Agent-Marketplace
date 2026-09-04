from ..base_service import Base
from models.schemas.memory_db_schema import (CreateMemory,GetMemory,UpdateMemory)
from sqlalchemy import select,update
from sqlalchemy.ext.asyncio import AsyncSession
from models.memory import Memory
from sqlalchemy.exc import SQLAlchemyError


class MemoryService(Base):
    def __init__(self,db:AsyncSession):
        super().__init__()
        self.db=db

    async def add_memory(self,data:CreateMemory)->Memory:
        self.logger.info("Starting memory creation")
        memory=Memory(conversation_id=data.conversation_id,summary=data.summary,last_message_id=data.last_message_id)
        try:
            self.db.add(memory)
            await self.db.commit()
            await self.db.refresh(memory)
            self.logger.info("Memory persisted to database successfully")
            return memory

        except SQLAlchemyError:
            await self.db.rollback()
            self.logger.error("Failed to create memory due to a database error", exc_info=True)
            raise

        except Exception:
            self.logger.error("Failed to create memory", exc_info=True)
            raise

    async def get_memory(self,info:GetMemory)->Memory| None:
        self.logger.info("Retrieving memory")
        
        try:

           stmt=select(Memory).where(Memory.conversation_id==info.conversation_id)

           result=await self.db.execute(stmt)
           self.logger.info("Finished retrieving")
           return result.scalar_one_or_none()

        except SQLAlchemyError:
            self.logger.error("Failed to retrieve memory due to a database error", exc_info=True)
            raise

        except Exception:
            self.logger.error("Failed to retrieve memory", exc_info=True)
            raise

    async def update_memory(self,info:UpdateMemory)->Memory| None:
        self.logger.info("Updating memory")
        
        try:

           stmt=update(Memory).where(Memory.conversation_id==info.conversation_id).values(summary=info.summary,last_message_id=info.last_message_id).returning(Memory)

           result=await self.db.execute(stmt)
           await self.db.commit()
           return result.scalar_one_or_none()

        except SQLAlchemyError:
            await self.db.rollback()
            self.logger.error("Failed to update memory due to a database error", exc_info=True)
            raise

        except Exception:
            self.logger.error("Failed to update memory", exc_info=True)
            raise