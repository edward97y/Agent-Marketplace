from db.base  import Base
from uuid import uuid4, UUID
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, func, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from .enums import PlanType

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.user import User
    from models.agent import Agent
    from models.knowledge_base import KnowledgeBase
    from models.conversation import Conversation
    from models.company_schema_mapping import CompanySchemaMapping


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    plan: Mapped[PlanType] = mapped_column(
        Enum(PlanType),
        nullable=False,
        default=PlanType.FREE.value
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    users: Mapped[list["User"]] = relationship(
        back_populates="company"
    )

    agents: Mapped[list["Agent"]] = relationship(
        back_populates="company"
    )

    knowledge_bases: Mapped[list["KnowledgeBase"]] = relationship(
        back_populates="company"
    )

    conversations: Mapped[list["Conversation"]] = relationship(
        back_populates="company"
    )
    schema_mappings: Mapped[list["CompanySchemaMapping"]] = relationship(
    back_populates="company"
)