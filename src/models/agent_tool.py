from db import Base
from uuid import uuid4, UUID
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, JSON, func, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.agent import Agent


class AgentTool(Base):
    __tablename__ = "agent_tools"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    agent_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("agents.id"),
        nullable=False
    )

    tool_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    configuration: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    agent: Mapped["Agent"] = relationship(
        back_populates="tools"
    )