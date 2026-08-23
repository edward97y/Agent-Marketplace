from db import Base
from uuid import uuid4, UUID
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.company import Company


class CompanySchemaMapping(Base):
    __tablename__ = "company_schema_mappings"

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

    mapping: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict
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

    company: Mapped["Company"] = relationship(
        back_populates="schema_mappings"
    )