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
            stmt = (select(Message)
                    .where(Message.conversation_id == info.conversation_id)
                    .order_by(Message.created_at))
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

    async def get_messages_for_summary(
    self,
    conversation_id: UUID,
    last_message_id: UUID,
    limit: int = 30,
    ):
        stmt = (
            select(Message)
            .where(
                Message.conversation_id == conversation_id,
                Message.created_at >= (
                    select(Message.created_at)
                    .where(Message.id == last_message_id)
                    .scalar_subquery()
                ),
            )
            .order_by(Message.created_at.asc())
            .limit(limit)
        )

        result = await self.db.execute(stmt)

        return result.scalars().all()
    
    async def get_messages_after(
    self,
    conversation_id: UUID,
    last_message_id: UUID | None,
) -> list[Message]:
        self.logger.info("Retrieving messages after last message")

        stmt = (
            select(Message)
            .where(
                Message.conversation_id == conversation_id
            )
            .order_by(Message.created_at.asc())
        )

        if last_message_id is not None:
            last_created_at = (
                select(Message.created_at)
                .where(Message.id == last_message_id)
                .scalar_subquery()
            )
            stmt = stmt.where(Message.created_at > last_created_at)

        result = await self.db.execute(stmt)
        self.logger.info(f"Finished retrieving messages")
        return result.scalars().all()