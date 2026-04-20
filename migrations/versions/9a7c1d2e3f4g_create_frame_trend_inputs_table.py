"""create frame_trend_inputs table

Revision ID: 9a7c1d2e3f4g
Revises: 8f3c2a1d4b7e
Create Date: 2026-04-07 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "9a7c1d2e3f4g"
down_revision = "8f3c2a1d4b7e"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "frame_trend_inputs",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("target_date", sa.Date(), nullable=False),
        sa.Column("venue", sa.String(length=50), nullable=False),
        sa.Column("race_number", sa.Integer(), nullable=False),
        sa.Column("winning_frame", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.UniqueConstraint(
            "target_date",
            "venue",
            "race_number",
            name="uq_frame_trend_input_target_date_venue_race_number",
        ),
    )

    op.create_index(
        "ix_frame_trend_inputs_target_date",
        "frame_trend_inputs",
        ["target_date"],
        unique=False,
    )
    op.create_index(
        "ix_frame_trend_inputs_venue",
        "frame_trend_inputs",
        ["venue"],
        unique=False,
    )


def downgrade():
    op.drop_index("ix_frame_trend_inputs_venue", table_name="frame_trend_inputs")
    op.drop_index("ix_frame_trend_inputs_target_date", table_name="frame_trend_inputs")
    op.drop_table("frame_trend_inputs")