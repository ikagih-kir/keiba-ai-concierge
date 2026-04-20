"""create condition change related tables

Revision ID: 20260401_create_condition_change_tables
Revises: <ここを既存の最新revisionに変更>
Create Date: 2026-04-01 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


revision = "8f3c2a1d4b7e"
down_revision = "add_assistant_messages"
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "races",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("race_key", sa.String(length=64), nullable=False),
        sa.Column("race_date", sa.Date(), nullable=False),
        sa.Column("venue", sa.String(length=50), nullable=False),
        sa.Column("race_number", sa.Integer(), nullable=False),
        sa.Column("race_name", sa.String(length=255), nullable=False),
        sa.Column("grade", sa.String(length=20), nullable=True),
        sa.Column("surface", sa.String(length=20), nullable=False),
        sa.Column("distance", sa.Integer(), nullable=False),
        sa.Column("direction", sa.String(length=20), nullable=True),
        sa.Column("course_class", sa.String(length=50), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("race_key", name="uq_races_race_key"),
    )
    op.create_index("ix_races_race_key", "races", ["race_key"], unique=False)
    op.create_index("ix_races_race_date", "races", ["race_date"], unique=False)

    op.create_table(
        "race_entries",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("race_id", sa.BigInteger(), nullable=False),
        sa.Column("horse_key", sa.String(length=64), nullable=False),
        sa.Column("horse_name", sa.String(length=255), nullable=False),
        sa.Column("frame_number", sa.Integer(), nullable=True),
        sa.Column("horse_number", sa.Integer(), nullable=True),
        sa.Column("sex", sa.String(length=10), nullable=True),
        sa.Column("age", sa.Integer(), nullable=True),
        sa.Column("jockey_name", sa.String(length=100), nullable=True),
        sa.Column("trainer_name", sa.String(length=100), nullable=True),
        sa.Column("handicap_weight", sa.DECIMAL(precision=4, scale=1), nullable=True),
        sa.Column("blinkers_now", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.Column("odds", sa.DECIMAL(precision=8, scale=2), nullable=True),
        sa.Column("popularity", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["race_id"], ["races.id"]),
        sa.UniqueConstraint("race_id", "horse_key", name="uq_race_entries_race_horse"),
    )
    op.create_index("ix_race_entries_race_id", "race_entries", ["race_id"], unique=False)
    op.create_index("ix_race_entries_horse_key", "race_entries", ["horse_key"], unique=False)

    op.create_table(
        "condition_change_horses",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("race_id", sa.BigInteger(), nullable=False),
        sa.Column("race_entry_id", sa.BigInteger(), nullable=False),
        sa.Column("horse_key", sa.String(length=64), nullable=False),
        sa.Column("horse_name", sa.String(length=255), nullable=False),
        sa.Column("prev_race_date", sa.Date(), nullable=True),
        sa.Column("prev_race_name", sa.String(length=255), nullable=True),
        sa.Column("prev_surface", sa.String(length=20), nullable=True),
        sa.Column("prev_distance", sa.Integer(), nullable=True),
        sa.Column("prev_finish_position", sa.Integer(), nullable=True),
        sa.Column("current_surface", sa.String(length=20), nullable=False),
        sa.Column("current_distance", sa.Integer(), nullable=False),
        sa.Column("distance_diff", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("surface_changed", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.Column("blinkers_first_time", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.Column("blinkers_reapplied", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.Column("blinkers_removed", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.Column("layoff_days", sa.Integer(), nullable=True),
        sa.Column("change_flags", mysql.JSON(), nullable=False),
        sa.Column("change_score", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("short_comment", sa.String(length=500), nullable=True),
        sa.Column("ai_comment", sa.Text(), nullable=True),
        sa.Column("is_featured", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.Column("display_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("batch_date", sa.Date(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["race_id"], ["races.id"]),
        sa.ForeignKeyConstraint(["race_entry_id"], ["race_entries.id"]),
    )
    op.create_index(
        "ix_condition_change_horses_race_id",
        "condition_change_horses",
        ["race_id"],
        unique=False,
    )
    op.create_index(
        "ix_condition_change_horses_race_entry_id",
        "condition_change_horses",
        ["race_entry_id"],
        unique=False,
    )
    op.create_index(
        "ix_condition_change_horses_horse_key",
        "condition_change_horses",
        ["horse_key"],
        unique=False,
    )
    op.create_index(
        "ix_condition_change_horses_batch_date",
        "condition_change_horses",
        ["batch_date"],
        unique=False,
    )
    op.create_index(
        "ix_condition_change_horses_is_featured",
        "condition_change_horses",
        ["is_featured"],
        unique=False,
    )


def downgrade():
    op.drop_index("ix_condition_change_horses_is_featured", table_name="condition_change_horses")
    op.drop_index("ix_condition_change_horses_batch_date", table_name="condition_change_horses")
    op.drop_index("ix_condition_change_horses_horse_key", table_name="condition_change_horses")
    op.drop_index("ix_condition_change_horses_race_entry_id", table_name="condition_change_horses")
    op.drop_index("ix_condition_change_horses_race_id", table_name="condition_change_horses")
    op.drop_table("condition_change_horses")

    op.drop_index("ix_race_entries_horse_key", table_name="race_entries")
    op.drop_index("ix_race_entries_race_id", table_name="race_entries")
    op.drop_table("race_entries")

    op.drop_index("ix_races_race_date", table_name="races")
    op.drop_index("ix_races_race_key", table_name="races")
    op.drop_table("races")