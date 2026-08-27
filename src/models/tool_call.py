from db.base  import Base
from uuid import uuid4, UUID
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, JSON, func, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.agent_run import AgentRun


class ToolCall(Base):
    __tablename__ = "tool_calls"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    run_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("agent_runs.id"),
        nullable=False
    )

    tool: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    input: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict
    )

    output: Mapped[dict | None] = mapped_column(
        JSON
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    run: Mapped["AgentRun"] = relationship(
        back_populates="tool_calls"
    )