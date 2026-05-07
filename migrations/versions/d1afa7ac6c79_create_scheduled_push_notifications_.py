"""create_scheduled_push_notifications_table

Revision ID: d1afa7ac6c79
Revises: 320b3caf89e7
Create Date: 2026-05-07 17:01:20.892643

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1afa7ac6c79'
down_revision: Union[str, None] = '320b3caf89e7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "scheduled_push_notifications",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("body", sa.String(length=255), nullable=False),
        sa.Column("target_path", sa.String(length=255), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="scheduled"),
        sa.Column("scheduled_at", sa.DateTime(), nullable=False),
        sa.Column("sent_at", sa.DateTime(), nullable=True),
        sa.Column("canceled_at", sa.DateTime(), nullable=True),
        sa.Column("success_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("failure_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("total_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
    )

    op.create_index(
        "ix_scheduled_push_notifications_status",
        "scheduled_push_notifications",
        ["status"],
    )
    op.create_index(
        "ix_scheduled_push_notifications_scheduled_at",
        "scheduled_push_notifications",
        ["scheduled_at"],
    )


def downgrade():
    op.drop_index("ix_scheduled_push_notifications_scheduled_at", table_name="scheduled_push_notifications")
    op.drop_index("ix_scheduled_push_notifications_status", table_name="scheduled_push_notifications")
    op.drop_table("scheduled_push_notifications")
