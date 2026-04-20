"""add assistant_messages

Revision ID: add_assistant_messages
Revises: add_race_change_and_frame_trends
Create Date: 2026-03-25 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "add_assistant_messages"
down_revision: Union[str, None] = "add_race_change_and_frame_trends"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "assistant_messages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("target_date", sa.Date(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("message_type", sa.String(length=50), nullable=True),
        sa.Column("priority", sa.Integer(), nullable=True, server_default="0"),
        sa.Column("sort_order", sa.Integer(), nullable=True, server_default="0"),
        sa.Column("is_featured", sa.Boolean(), nullable=True, server_default=sa.text("0")),
        sa.Column("is_public", sa.Boolean(), nullable=True, server_default=sa.text("1")),
        sa.Column("action_type", sa.String(length=20), nullable=True),
        sa.Column("action_label", sa.String(length=100), nullable=True),
        sa.Column("action_path", sa.String(length=255), nullable=True),
        sa.Column("target_segment", sa.String(length=50), nullable=True),
        sa.Column("related_content_type", sa.String(length=50), nullable=True),
        sa.Column("related_content_id", sa.Integer(), nullable=True),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_assistant_messages_id"),
        "assistant_messages",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_assistant_messages_target_date"),
        "assistant_messages",
        ["target_date"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_assistant_messages_target_date"), table_name="assistant_messages")
    op.drop_index(op.f("ix_assistant_messages_id"), table_name="assistant_messages")
    op.drop_table("assistant_messages")