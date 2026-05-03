"""create_home_dialogs_table

Revision ID: 7612ef0faa9b
Revises: 1834c1365808
Create Date: 2026-05-03 21:35:57.426803

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7612ef0faa9b'
down_revision: Union[str, None] = '1834c1365808'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "home_dialogs",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("primary_button_text", sa.String(length=50), nullable=True),
        sa.Column("primary_button_path", sa.String(length=255), nullable=True),
        sa.Column("secondary_button_text", sa.String(length=50), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("show_once_per_day", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("start_at", sa.DateTime(), nullable=True),
        sa.Column("end_at", sa.DateTime(), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
    )

    op.create_index("ix_home_dialogs_is_active", "home_dialogs", ["is_active"])
    op.create_index("ix_home_dialogs_sort_order", "home_dialogs", ["sort_order"])


def downgrade():
    op.drop_index("ix_home_dialogs_sort_order", table_name="home_dialogs")
    op.drop_index("ix_home_dialogs_is_active", table_name="home_dialogs")
    op.drop_table("home_dialogs")