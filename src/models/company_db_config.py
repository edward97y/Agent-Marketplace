from db.base import Base
from uuid import uuid4, UUID
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, func, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from .enums import DatabaseType

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.company import Company


class CompanyDBConfig(Base):
    __tablename__ = "company_db_configs"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    company_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("companies.id"),
        nullable=False,
        unique=True
    )

    host: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    username: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    port: Mapped[int] = mapped_column(
    nullable=False
)

    type: Mapped[DatabaseType] = mapped_column(
        Enum(DatabaseType),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    company: Mapped["Company"] = relationship(
        back_populates="db_config"
    )