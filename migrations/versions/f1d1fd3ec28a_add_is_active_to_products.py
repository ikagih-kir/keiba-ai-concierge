"""add is_active to products

Revision ID: f1d1fd3ec28a
Revises: 42b2a4473a5f
Create Date: 2026-01-28 13:00:01.097349

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f1d1fd3ec28a'
down_revision: Union[str, None] = '42b2a4473a5f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
