from ..base_service import Base
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.message import Message
from sqlalchemy.exc import SQLAlchemyError
from models.schemas.messages_routes_schema import (GetMessages,MessageResponse)
from uuid import UUID
from models.enums.db_enum import MessageRole
class MessageDBService(Base):
    def __init__(self,db:AsyncSession):
        super().__init__()
        self.db=db

    
    async def get_messages(self, info: GetMessages)->MessageResponse:
        self.logger.info("Retrieving messages for conversation")
        try:
            stmt = select(Message).where(Message.conversation_id == info.conversation_id)
            result = await self.db.execute(stmt)
            messages = result.scalars().all()
            self.logger.info(f"Retrieved {len(messages)} messages")
            return messages

        except SQLAlchemyError:
            self.logger.error(
                f"Database error retrieving messages ",
                exc_info=True,
            )
            raise

        except Exception:
            self.logger.error(
                f"Unexpected error retrieving messages",
                exc_info=True,
            )
            raise

    async def save_user_message(self,content:str,conversation_id:UUID):
            self.logger.info("Saving user message")
            message=Message(conversation_id=conversation_id,content=content,
                            role=MessageRole.USER)
            try:
                self.db.add(message)
                await self.db.commit()
                await self.db.refresh(message)
                self.logger.info("User message persisted to database")
                return message
            except SQLAlchemyError:
                await self.db.rollback()
                self.logger.error(
                    f"Database error saving user message ",
                    exc_info=True,
                )
                raise
    
            except Exception:
                self.logger.error(
                    f"Unexpected error saving user message ",
                    exc_info=True,
                )
                raise
    
    