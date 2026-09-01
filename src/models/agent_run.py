from db.base  import Base
from uuid import uuid4, UUID
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from .enums import RunStatus

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.conversation import Conversation
    from models.agent import Agent
    from models.tool_call import ToolCall
    from models.evaluation import Evaluation
    from models.event_log import EventLog


class AgentRun(Base):
    __tablename__ = "agent_runs"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    conversation_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("conversations.id"),
        nullable=False
    )

    agent_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("agents.id"),
        nullable=False
    )

    status: Mapped[RunStatus] = mapped_column(
        Enum(RunStatus),
        nullable=False,
        default=RunStatus.PENDING.value
    )
    

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    
    updated_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now()
        )

    conversation: Mapped["Conversation"] = relationship(
        back_populates="runs"
    )

    agent: Mapped["Agent"] = relationship(
        back_populates="runs"
    )

    tool_calls: Mapped[list["ToolCall"]] = relationship(
        back_populates="run"
    )

    evaluations: Mapped[list["Evaluation"]] = relationship(
        back_populates="run"
    )

    events: Mapped[list["EventLog"]] = relationship(
        back_populates="run"
    )