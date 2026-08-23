from db import Base
from uuid import uuid4, UUID
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.company import Company
    from models.user import User
    from models.agent import Agent
    from models.message import Message
    from models.memory import Memory
    from models.agent_run import AgentRun


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    company_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("companies.id"),
        nullable=False
    )

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    agent_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("agents.id"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    company: Mapped["Company"] = relationship(
        back_populates="conversations"
    )

    user: Mapped["User"] = relationship(
        back_populates="conversations"
    )

    agent: Mapped["Agent"] = relationship(
        back_populates="conversations"
    )

    messages: Mapped[list["Message"]] = relationship(
        back_populates="conversation"
    )

    memories: Mapped[list["Memory"]] = relationship(
        back_populates="conversation"
    )

    runs: Mapped[list["AgentRun"]] = relationship(
        back_populates="conversation"
    )