"""add_placement_to_home_banners

Revision ID: 624abff97f66
Revises: babd1da2e37a
Create Date: 2026-07-05 23:05:32.217139

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '624abff97f66'
down_revision: Union[str, None] = 'babd1da2e37a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "home_banners",
        sa.Column(
            "placement",
            sa.String(length=50),
            nullable=False,
            server_default="home_middle",
        ),
    )


def downgrade():
    op.drop_column("home_banners", "placement")
