"""add race_change_highlights and frame_trend_snapshots

Revision ID: add_race_change_and_frame_trends
Revises: 
Create Date: 2026-03-24 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "add_race_change_and_frame_trends"
down_revision: Union[str, None] = "xxxx_extend_products"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "race_change_highlights",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("target_date", sa.Date(), nullable=False),
        sa.Column("race_name", sa.String(length=255), nullable=False),
        sa.Column("race_course", sa.String(length=100), nullable=True),
        sa.Column("horse_name", sa.String(length=255), nullable=False),
        sa.Column("previous_surface", sa.String(length=20), nullable=True),
        sa.Column("current_surface", sa.String(length=20), nullable=True),
        sa.Column("previous_distance", sa.Integer(), nullable=True),
        sa.Column("current_distance", sa.Integer(), nullable=True),
        sa.Column("previous_jockey", sa.String(length=100), nullable=True),
        sa.Column("current_jockey", sa.String(length=100), nullable=True),
        sa.Column("surface_changed", sa.Boolean(), nullable=True, server_default=sa.text("0")),
        sa.Column("distance_changed", sa.Boolean(), nullable=True, server_default=sa.text("0")),
        sa.Column("distance_direction", sa.String(length=20), nullable=True),
        sa.Column("gear_changed", sa.Boolean(), nullable=True, server_default=sa.text("0")),
        sa.Column("jockey_changed", sa.Boolean(), nullable=True, server_default=sa.text("0")),
        sa.Column("class_changed", sa.Boolean(), nullable=True, server_default=sa.text("0")),
        sa.Column("change_summary", sa.String(length=255), nullable=True),
        sa.Column("ai_comment", sa.Text(), nullable=True),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("impact_level", sa.String(length=20), nullable=True),
        sa.Column("is_featured", sa.Boolean(), nullable=True, server_default=sa.text("0")),
        sa.Column("sort_order", sa.Integer(), nullable=True, server_default="0"),
        sa.Column("is_public", sa.Boolean(), nullable=True, server_default=sa.text("1")),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_race_change_highlights_id"),
        "race_change_highlights",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_race_change_highlights_target_date"),
        "race_change_highlights",
        ["target_date"],
        unique=False,
    )

    op.create_table(
        "frame_trend_snapshots",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("target_date", sa.Date(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("race_scope", sa.String(length=100), nullable=True),
        sa.Column("lucky_frame", sa.Integer(), nullable=True),
        sa.Column("trend_summary", sa.String(length=255), nullable=True),
        sa.Column("trend_note", sa.Text(), nullable=True),
        sa.Column("recommended_style", sa.String(length=20), nullable=True),
        sa.Column("sample_size", sa.Integer(), nullable=True),
        sa.Column("win_frame_data", sa.Text(), nullable=True),
        sa.Column("place_frame_data", sa.Text(), nullable=True),
        sa.Column("ai_comment", sa.Text(), nullable=True),
        sa.Column("is_featured", sa.Boolean(), nullable=True, server_default=sa.text("0")),
        sa.Column("sort_order", sa.Integer(), nullable=True, server_default="0"),
        sa.Column("is_public", sa.Boolean(), nullable=True, server_default=sa.text("1")),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_frame_trend_snapshots_id"),
        "frame_trend_snapshots",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_frame_trend_snapshots_target_date"),
        "frame_trend_snapshots",
        ["target_date"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_frame_trend_snapshots_target_date"), table_name="frame_trend_snapshots")
    op.drop_index(op.f("ix_frame_trend_snapshots_id"), table_name="frame_trend_snapshots")
    op.drop_table("frame_trend_snapshots")

    op.drop_index(op.f("ix_race_change_highlights_target_date"), table_name="race_change_highlights")
    op.drop_index(op.f("ix_race_change_highlights_id"), table_name="race_change_highlights")
    op.drop_table("race_change_highlights")