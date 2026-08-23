from db import Base
from uuid import uuid4, UUID
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, func, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from .enums import UserRole

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.company import Company
    from models.conversation import Conversation


class User(Base):
    __tablename__ = "users"

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

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        nullable=False,
        default=UserRole.MEMBER.value
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    company: Mapped["Company"] = relationship(
        back_populates="users"
    )

    conversations: Mapped[list["Conversation"]] = relationship(
        back_populates="user"
    )