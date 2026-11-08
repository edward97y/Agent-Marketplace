from db.base  import Base
from uuid import uuid4, UUID
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, Integer, func, DateTime, ForeignKey, Computed, Index
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, TSVECTOR

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
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default="0"
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    # keyword (full text) side of the hybrid search.
    # postgres generates it automatically from content, we never write it.
    # 'simple' config = no stemming / no stop words so it works for arabic and english
    search_vector: Mapped[str] = mapped_column(
        TSVECTOR,
        Computed("to_tsvector('simple', content)", persisted=True),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    document: Mapped["Document"] = relationship(
        back_populates="chunks"
    )

    embeddings: Mapped[list["Embedding"]] = relationship(
        back_populates="chunk",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    __table_args__ = (
        Index(
            "ix_document_chunks_search_vector",
            "search_vector",
            postgresql_using="gin"
        ),
    )
