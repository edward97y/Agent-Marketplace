"""add rag hybrid search (full text column, vector index, cascades)

Revision ID: a7c3e9f1b2d4
Revises: d2d0e0182358
Create Date: 2026-11-08 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'a7c3e9f1b2d4'
down_revision: Union[str, Sequence[str], None] = 'd2d0e0182358'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    # ---------- document_chunks: order + full text search column ----------
    op.add_column('document_chunks',
                  sa.Column('chunk_index', sa.Integer(), server_default='0', nullable=False))
    op.add_column('document_chunks',
                  sa.Column('search_vector', postgresql.TSVECTOR(),
                            sa.Computed("to_tsvector('simple', content)", persisted=True),
                            nullable=True))
    op.create_index('ix_document_chunks_search_vector', 'document_chunks',
                    ['search_vector'], unique=False, postgresql_using='gin')

    # ---------- embeddings: approximate nearest neighbour index ----------
    op.create_index('ix_embeddings_embedding_hnsw', 'embeddings', ['embedding'], unique=False,
                    postgresql_using='hnsw',
                    postgresql_with={'m': 16, 'ef_construction': 64},
                    postgresql_ops={'embedding': 'vector_cosine_ops'})

    # ---------- foreign key indexes (used by the joins in hybrid search) ----------
    op.create_index(op.f('ix_documents_knowledge_base_id'), 'documents', ['knowledge_base_id'], unique=False)
    op.create_index(op.f('ix_document_chunks_document_id'), 'document_chunks', ['document_id'], unique=False)
    op.create_index(op.f('ix_embeddings_chunk_id'), 'embeddings', ['chunk_id'], unique=False)

    # ---------- cascade deletes: knowledge base -> documents -> chunks -> embeddings ----------
    op.drop_constraint('documents_knowledge_base_id_fkey', 'documents', type_='foreignkey')
    op.create_foreign_key('documents_knowledge_base_id_fkey', 'documents', 'knowledge_bases',
                          ['knowledge_base_id'], ['id'], ondelete='CASCADE')

    op.drop_constraint('document_chunks_document_id_fkey', 'document_chunks', type_='foreignkey')
    op.create_foreign_key('document_chunks_document_id_fkey', 'document_chunks', 'documents',
                          ['document_id'], ['id'], ondelete='CASCADE')

    op.drop_constraint('embeddings_chunk_id_fkey', 'embeddings', type_='foreignkey')
    op.create_foreign_key('embeddings_chunk_id_fkey', 'embeddings', 'document_chunks',
                          ['chunk_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('embeddings_chunk_id_fkey', 'embeddings', type_='foreignkey')
    op.create_foreign_key('embeddings_chunk_id_fkey', 'embeddings', 'document_chunks',
                          ['chunk_id'], ['id'])

    op.drop_constraint('document_chunks_document_id_fkey', 'document_chunks', type_='foreignkey')
    op.create_foreign_key('document_chunks_document_id_fkey', 'document_chunks', 'documents',
                          ['document_id'], ['id'])

    op.drop_constraint('documents_knowledge_base_id_fkey', 'documents', type_='foreignkey')
    op.create_foreign_key('documents_knowledge_base_id_fkey', 'documents', 'knowledge_bases',
                          ['knowledge_base_id'], ['id'])

    op.drop_index(op.f('ix_embeddings_chunk_id'), table_name='embeddings')
    op.drop_index(op.f('ix_document_chunks_document_id'), table_name='document_chunks')
    op.drop_index(op.f('ix_documents_knowledge_base_id'), table_name='documents')

    op.drop_index('ix_embeddings_embedding_hnsw', table_name='embeddings')

    op.drop_index('ix_document_chunks_search_vector', table_name='document_chunks')
    op.drop_column('document_chunks', 'search_vector')
    op.drop_column('document_chunks', 'chunk_index')
