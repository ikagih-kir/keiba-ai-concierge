"""create_push_tokens_table

Revision ID: 320b3caf89e7
Revises: 7612ef0faa9b
Create Date: 2026-05-06 11:04:04.930161

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '320b3caf89e7'
down_revision: Union[str, None] = '7612ef0faa9b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "push_tokens",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("device_id", sa.String(length=255), nullable=True),
        sa.Column("fcm_token", sa.Text(), nullable=False),
        sa.Column("platform", sa.String(length=20), nullable=True),
        sa.Column("app_version", sa.String(length=50), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
    )

    op.create_index("ix_push_tokens_device_id", "push_tokens", ["device_id"])
    op.create_index("ix_push_tokens_is_active", "push_tokens", ["is_active"])


def downgrade():
    op.drop_index("ix_push_tokens_is_active", table_name="push_tokens")
    op.drop_index("ix_push_tokens_device_id", table_name="push_tokens")
    op.drop_table("push_tokens")