# migrations/versions/xxxx_extend_products_for_campaign.py
from alembic import op
import sqlalchemy as sa

revision = "xxxx_extend_products"
down_revision = "040a49ea69ac"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("products", sa.Column("category_id", sa.Integer(), nullable=True))
    op.add_column("products", sa.Column("label", sa.String(length=255), nullable=True))
    op.add_column("products", sa.Column("status", sa.Enum("draft", "public", "private"), server_default="draft"))
    op.add_column("products", sa.Column("publish_start_at", sa.DateTime(), nullable=True))
    op.add_column("products", sa.Column("publish_end_at", sa.DateTime(), nullable=True))
    op.add_column("products", sa.Column("sold_out", sa.Boolean(), server_default=sa.false()))
    op.add_column("products", sa.Column("sold_out_at", sa.DateTime(), nullable=True))

    op.add_column("products", sa.Column("race_count", sa.Integer(), nullable=True))
    op.add_column("products", sa.Column("race_date", sa.String(length=50), nullable=True))
    op.add_column("products", sa.Column("ticket_type", sa.String(length=50), nullable=True))

    op.add_column("products", sa.Column("expected_return", sa.Integer(), nullable=True))
    op.add_column("products", sa.Column("max_return", sa.Integer(), nullable=True))

    op.add_column("products", sa.Column("recommended_amount", sa.String(length=50), nullable=True))
    op.add_column("products", sa.Column("recommended_race_count", sa.Integer(), nullable=True))
    op.add_column("products", sa.Column("capacity", sa.Integer(), nullable=True))


def downgrade():
    op.drop_column("products", "capacity")
    op.drop_column("products", "recommended_race_count")
    op.drop_column("products", "recommended_amount")
    op.drop_column("products", "max_return")
    op.drop_column("products", "expected_return")
    op.drop_column("products", "ticket_type")
    op.drop_column("products", "race_date")
    op.drop_column("products", "race_count")
    op.drop_column("products", "sold_out_at")
    op.drop_column("products", "sold_out")
    op.drop_column("products", "publish_end_at")
    op.drop_column("products", "publish_start_at")
    op.drop_column("products", "status")
    op.drop_column("products", "label")
    op.drop_column("products", "category_id")
