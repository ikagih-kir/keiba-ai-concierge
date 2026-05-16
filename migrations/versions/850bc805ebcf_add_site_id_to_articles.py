"""add_site_id_to_articles

Revision ID: 850bc805ebcf
Revises: d1afa7ac6c79
Create Date: 2026-05-16 11:25:11.712296

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


# revision identifiers, used by Alembic.
revision = "850bc805ebcf"
down_revision = "d1afa7ac6c79"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "articles",
        sa.Column("site_id", mysql.BIGINT(unsigned=True), nullable=True),
    )

    op.create_index(
        "ix_articles_site_id",
        "articles",
        ["site_id"],
    )

    op.create_foreign_key(
        "fk_articles_site_id_sites",
        "articles",
        "sites",
        ["site_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade():
    op.drop_constraint(
        "fk_articles_site_id_sites",
        "articles",
        type_="foreignkey",
    )
    op.drop_index("ix_articles_site_id", table_name="articles")
    op.drop_column("articles", "site_id")