"""create analytics events table

Revision ID: 20260223_000001
Revises:
Create Date: 2026-02-23 00:00:01
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20260223_000001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "analytics_events",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("source", sa.String(length=64), nullable=False),
        sa.Column("update_type", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("command_name", sa.String(length=128), nullable=True),
        sa.Column("callback_data", sa.String(length=256), nullable=True),
        sa.Column("handler_name", sa.String(length=255), nullable=True),
        sa.Column("duration_ms", sa.Integer(), nullable=True),
        sa.Column("user_id", sa.BigInteger(), nullable=True),
        sa.Column("username", sa.String(length=255), nullable=True),
        sa.Column("chat_id", sa.BigInteger(), nullable=True),
        sa.Column("error_type", sa.String(length=255), nullable=True),
        sa.Column("error_message", sa.String(length=1024), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_analytics_events_created_at", "analytics_events", ["created_at"], unique=False)
    op.create_index("ix_analytics_events_status_created_at", "analytics_events", ["status", "created_at"], unique=False)
    op.create_index(
        "ix_analytics_events_command_name_created_at",
        "analytics_events",
        ["command_name", "created_at"],
        unique=False,
    )
    op.create_index(
        "ix_analytics_events_callback_data_created_at",
        "analytics_events",
        ["callback_data", "created_at"],
        unique=False,
    )
    op.create_index("ix_analytics_events_user_id_created_at", "analytics_events", ["user_id", "created_at"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_analytics_events_user_id_created_at", table_name="analytics_events")
    op.drop_index("ix_analytics_events_callback_data_created_at", table_name="analytics_events")
    op.drop_index("ix_analytics_events_command_name_created_at", table_name="analytics_events")
    op.drop_index("ix_analytics_events_status_created_at", table_name="analytics_events")
    op.drop_index("ix_analytics_events_created_at", table_name="analytics_events")
    op.drop_table("analytics_events")
