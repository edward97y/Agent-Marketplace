from db.base  import Base
from uuid import uuid4, UUID
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, func, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.knowledge_base import KnowledgeBase
    from models.document_chunk import DocumentChunk


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    knowledge_base_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("knowledge_bases.id"),
        nullable=False
    )

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    knowledge_base: Mapped["KnowledgeBase"] = relationship(
        back_populates="documents"
    )

    chunks: Mapped[list["DocumentChunk"]] = relationship(
        back_populates="document"
    )