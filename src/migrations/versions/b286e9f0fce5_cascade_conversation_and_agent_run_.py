"""cascade conversation and agent run children

Deleting a conversation failed with a FK violation as soon as the agent had
run in it. A conversation owns its messages, memories and agent runs, and a
run owns its tool calls, event logs and evaluations, so they cascade.

Revision ID: b286e9f0fce5
Revises: a7c3e9f1b2d4
Create Date: 2026-11-08 14:34:24.101747

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'b286e9f0fce5'
down_revision: Union[str, Sequence[str], None] = 'a7c3e9f1b2d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# (constraint name, child table, parent table, child column)
FOREIGN_KEYS = [
    ('agent_runs_conversation_id_fkey', 'agent_runs', 'conversations', 'conversation_id'),
    ('messages_conversation_id_fkey', 'messages', 'conversations', 'conversation_id'),
    ('memories_conversation_id_fkey', 'memories', 'conversations', 'conversation_id'),
    ('tool_calls_run_id_fkey', 'tool_calls', 'agent_runs', 'run_id'),
    ('event_logs_run_id_fkey', 'event_logs', 'agent_runs', 'run_id'),
    ('evaluations_run_id_fkey', 'evaluations', 'agent_runs', 'run_id'),
]


def _recreate(ondelete: str | None) -> None:
    for name, child, parent, column in FOREIGN_KEYS:
        op.drop_constraint(name, child, type_='foreignkey')
        op.create_foreign_key(name, child, parent, [column], ['id'], ondelete=ondelete)


def upgrade() -> None:
    _recreate(ondelete='CASCADE')


def downgrade() -> None:
    _recreate(ondelete=None)
