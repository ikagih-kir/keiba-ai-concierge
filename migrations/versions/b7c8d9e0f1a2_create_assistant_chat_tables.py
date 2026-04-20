"""create assistant chat tables

Revision ID: b7c8d9e0f1a2
Revises: <今の最新revisionに変更>
Create Date: 2026-04-11 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "b7c8d9e0f1a2"
down_revision = "a1b2c3d4e5f6"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "chat_threads",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.BigInteger(), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=True),
        sa.Column("last_user_message", sa.String(length=1000), nullable=True),
        sa.Column("message_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_chat_threads_user_id", "chat_threads", ["user_id"], unique=False)

    op.create_table(
        "chat_faqs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("question_pattern", sa.String(length=255), nullable=False),
        sa.Column("normalized_question", sa.String(length=500), nullable=False),
        sa.Column("intent", sa.String(length=100), nullable=False),
        sa.Column("sub_intent", sa.String(length=100), nullable=True),
        sa.Column("answer_title", sa.String(length=255), nullable=True),
        sa.Column("answer_text", sa.Text(), nullable=False),
        sa.Column("suggested_actions_json", sa.Text(), nullable=True),
        sa.Column("keywords_json", sa.Text(), nullable=True),
        sa.Column("priority", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("usage_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_used_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_chat_faqs_normalized_question", "chat_faqs", ["normalized_question"], unique=False)
    op.create_index("ix_chat_faqs_intent", "chat_faqs", ["intent"], unique=False)
    op.create_index("ix_chat_faqs_sub_intent", "chat_faqs", ["sub_intent"], unique=False)

    op.create_table(
        "chat_messages",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("thread_id", sa.Integer(), sa.ForeignKey("chat_threads.id", ondelete="CASCADE"), nullable=False),
        sa.Column("role", sa.String(length=20), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("intent", sa.String(length=100), nullable=True),
        sa.Column("normalized_question", sa.String(length=500), nullable=True),
        sa.Column("answered_by", sa.String(length=50), nullable=True),
        sa.Column("source_summary", sa.String(length=255), nullable=True),
        sa.Column("suggested_actions_json", sa.Text(), nullable=True),
        sa.Column("model_name", sa.String(length=100), nullable=True),
        sa.Column("response_ms", sa.Integer(), nullable=True),
        sa.Column("user_id", sa.BigInteger(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_chat_messages_thread_id", "chat_messages", ["thread_id"], unique=False)
    op.create_index("ix_chat_messages_intent", "chat_messages", ["intent"], unique=False)
    op.create_index("ix_chat_messages_answered_by", "chat_messages", ["answered_by"], unique=False)
    op.create_index("ix_chat_messages_user_id", "chat_messages", ["user_id"], unique=False)

    op.create_table(
        "chat_question_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("thread_id", sa.Integer(), sa.ForeignKey("chat_threads.id", ondelete="SET NULL"), nullable=True),
        sa.Column("message_id", sa.Integer(), sa.ForeignKey("chat_messages.id", ondelete="SET NULL"), nullable=True),
        sa.Column("user_id", sa.BigInteger(), nullable=True),
        sa.Column("raw_question", sa.Text(), nullable=False),
        sa.Column("normalized_question", sa.String(length=500), nullable=True),
        sa.Column("intent", sa.String(length=100), nullable=True),
        sa.Column("sub_intent", sa.String(length=100), nullable=True),
        sa.Column("answered_by", sa.String(length=50), nullable=True),
        sa.Column("faq_id", sa.Integer(), sa.ForeignKey("chat_faqs.id", ondelete="SET NULL"), nullable=True),
        sa.Column("is_answered_successfully", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("needs_improvement", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("feedback_score", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_chat_question_logs_thread_id", "chat_question_logs", ["thread_id"], unique=False)
    op.create_index("ix_chat_question_logs_message_id", "chat_question_logs", ["message_id"], unique=False)
    op.create_index("ix_chat_question_logs_user_id", "chat_question_logs", ["user_id"], unique=False)
    op.create_index("ix_chat_question_logs_normalized_question", "chat_question_logs", ["normalized_question"], unique=False)
    op.create_index("ix_chat_question_logs_intent", "chat_question_logs", ["intent"], unique=False)
    op.create_index("ix_chat_question_logs_sub_intent", "chat_question_logs", ["sub_intent"], unique=False)
    op.create_index("ix_chat_question_logs_answered_by", "chat_question_logs", ["answered_by"], unique=False)
    op.create_index("ix_chat_question_logs_faq_id", "chat_question_logs", ["faq_id"], unique=False)


def downgrade():
    op.drop_index("ix_chat_question_logs_faq_id", table_name="chat_question_logs")
    op.drop_index("ix_chat_question_logs_answered_by", table_name="chat_question_logs")
    op.drop_index("ix_chat_question_logs_sub_intent", table_name="chat_question_logs")
    op.drop_index("ix_chat_question_logs_intent", table_name="chat_question_logs")
    op.drop_index("ix_chat_question_logs_normalized_question", table_name="chat_question_logs")
    op.drop_index("ix_chat_question_logs_user_id", table_name="chat_question_logs")
    op.drop_index("ix_chat_question_logs_message_id", table_name="chat_question_logs")
    op.drop_index("ix_chat_question_logs_thread_id", table_name="chat_question_logs")
    op.drop_table("chat_question_logs")

    op.drop_index("ix_chat_messages_user_id", table_name="chat_messages")
    op.drop_index("ix_chat_messages_answered_by", table_name="chat_messages")
    op.drop_index("ix_chat_messages_intent", table_name="chat_messages")
    op.drop_index("ix_chat_messages_thread_id", table_name="chat_messages")
    op.drop_table("chat_messages")

    op.drop_index("ix_chat_faqs_sub_intent", table_name="chat_faqs")
    op.drop_index("ix_chat_faqs_intent", table_name="chat_faqs")
    op.drop_index("ix_chat_faqs_normalized_question", table_name="chat_faqs")
    op.drop_table("chat_faqs")

    op.drop_index("ix_chat_threads_user_id", table_name="chat_threads")
    op.drop_table("chat_threads")