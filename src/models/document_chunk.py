from db import Base
from uuid import uuid4, UUID
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, func, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.document import Document
    from models.embedding import Embedding


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    document_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("documents.id"),
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    document: Mapped["Document"] = relationship(
        back_populates="chunks"
    )

    embeddings: Mapped[list["Embedding"]] = relationship(
        back_populates="chunk"
    )