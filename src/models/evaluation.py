from db import Base
from uuid import uuid4, UUID
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Float, func, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.agent_run import AgentRun


class Evaluation(Base):
    __tablename__ = "evaluations"

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

    score: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    run: Mapped["AgentRun"] = relationship(
        back_populates="evaluations"
    )