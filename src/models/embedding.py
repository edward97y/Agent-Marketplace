from db.base  import Base
from uuid import uuid4, UUID
from datetime import datetime
from helpers import get_settings
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from pgvector.sqlalchemy import Vector

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.document_chunk import DocumentChunk

 
settings=get_settings()

class Embedding(Base):
    __tablename__ = "embeddings"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    chunk_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("document_chunks.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    embedding: Mapped[list[float]] = mapped_column(
        Vector(settings.EMBEDDING_SIZE),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    chunk: Mapped["DocumentChunk"] = relationship(
        back_populates="embeddings"
    )

    __table_args__ = (
        # semantic side of the hybrid search (approximate nearest neighbour on cosine distance)
        Index(
            "ix_embeddings_embedding_hnsw",
            "embedding",
            postgresql_using="hnsw",
            postgresql_with={"m": 16, "ef_construction": 64},
            postgresql_ops={"embedding": "vector_cosine_ops"}
        ),
    )
