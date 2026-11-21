"""add messages conversation_id created_at index

Revision ID: e8b4c2a1d9f3
Revises: b286e9f0fce5
Create Date: 2026-11-17 13:30:00.000000

"""
from typing import Sequence, Union

from alembic import op


revision: str = 'e8b4c2a1d9f3'
down_revision: Union[str, Sequence[str], None] = 'b286e9f0fce5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index('ix_messages_conversation_id_created_at', 'messages',
                    ['conversation_id', 'created_at'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_messages_conversation_id_created_at', table_name='messages')
