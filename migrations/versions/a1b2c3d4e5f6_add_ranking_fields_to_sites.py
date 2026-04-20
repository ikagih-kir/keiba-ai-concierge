"""add ranking fields to sites

Revision ID: a1b2c3d4e5f6
Revises: 9a7c1d2e3f4g
Create Date: 2026-04-08 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "a1b2c3d4e5f6"
down_revision = "9a7c1d2e3f4g"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "sites",
        sa.Column("hit_amount", sa.BigInteger(), nullable=False, server_default="0"),
    )
    op.add_column(
        "sites",
        sa.Column("hit_rate", sa.Numeric(5, 2), nullable=False, server_default="0"),
    )
    op.add_column(
        "sites",
        sa.Column("recovery_rate", sa.Numeric(6, 2), nullable=False, server_default="0"),
    )


def downgrade():
    op.drop_column("sites", "recovery_rate")
    op.drop_column("sites", "hit_rate")
    op.drop_column("sites", "hit_amount")