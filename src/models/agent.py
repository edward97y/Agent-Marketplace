from db import Base
from uuid import uuid4, UUID
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, func, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from .enums import AgentType

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.company import Company
    from models.agent_version import AgentVersion
    from models.agent_tool import AgentTool
    from models.agent_run import AgentRun
    from models.conversation import Conversation


class Agent(Base):
    __tablename__ = "agents"

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

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    description: Mapped[str | None]

    type: Mapped[AgentType] = mapped_column(
        Enum(AgentType),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    company: Mapped["Company"] = relationship(
        back_populates="agents"
    )

    versions: Mapped[list["AgentVersion"]] = relationship(
        back_populates="agent"
    )

    tools: Mapped[list["AgentTool"]] = relationship(
        back_populates="agent"
    )

    runs: Mapped[list["AgentRun"]] = relationship(
        back_populates="agent"
    )

    conversations: Mapped[list["Conversation"]] = relationship(
        back_populates="agent"
    )