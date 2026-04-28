"""create_jockey_trends_table

Revision ID: 1834c1365808
Revises: 00d704753e02
Create Date: 2026-04-28 09:08:44.324142
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "1834c1365808"
down_revision: Union[str, None] = "00d704753e02"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "jockey_trends",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("race_date", sa.Date(), nullable=False),
        sa.Column("venue", sa.String(length=50), nullable=True),
        sa.Column("meeting_type", sa.String(length=20), nullable=False, server_default="central"),
        sa.Column("race_no", sa.Integer(), nullable=False),
        sa.Column("race_name", sa.String(length=100), nullable=True),
        sa.Column("jockey_name", sa.String(length=100), nullable=False),
        sa.Column("horse_name", sa.String(length=100), nullable=True),
        sa.Column("memo", sa.Text(), nullable=True),
        sa.Column("is_published", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_index("ix_jockey_trends_race_date", "jockey_trends", ["race_date"])
    op.create_index("ix_jockey_trends_venue", "jockey_trends", ["venue"])
    op.create_index("ix_jockey_trends_meeting_type", "jockey_trends", ["meeting_type"])
    op.create_index("ix_jockey_trends_jockey_name", "jockey_trends", ["jockey_name"])
    op.create_index("ix_jockey_trends_is_published", "jockey_trends", ["is_published"])


def downgrade():
    op.drop_index("ix_jockey_trends_is_published", table_name="jockey_trends")
    op.drop_index("ix_jockey_trends_jockey_name", table_name="jockey_trends")
    op.drop_index("ix_jockey_trends_meeting_type", table_name="jockey_trends")
    op.drop_index("ix_jockey_trends_venue", table_name="jockey_trends")
    op.drop_index("ix_jockey_trends_race_date", table_name="jockey_trends")
    op.drop_table("jockey_trends")