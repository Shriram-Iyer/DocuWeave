"""Initial schema: templates, components, data_sources, link_configs

Revision ID: 0001
Revises:
Create Date: 2026-05-01
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "templates",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("output_format", sa.String(10), nullable=False, server_default="docx"),
        sa.Column("excel_config", sa.JSON(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )

    op.create_table(
        "template_components",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "template_id",
            sa.String(36),
            sa.ForeignKey("templates.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("type", sa.String(50), nullable=False),
        sa.Column("position", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("content", sa.Text(), nullable=False, server_default=""),
        sa.Column("source_table", sa.String(255), nullable=False, server_default=""),
        sa.Column("source_field", sa.String(255), nullable=False, server_default=""),
        sa.Column("columns", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("repeat_over", sa.String(255), nullable=False, server_default=""),
        sa.Column("transformations", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
    )
    op.create_index("ix_template_components_template_id", "template_components", ["template_id"])

    op.create_table(
        "data_sources",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("db_type", sa.String(20), nullable=False),
        sa.Column("db_url", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )

    op.create_table(
        "link_configs",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("tables", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )


def downgrade() -> None:
    op.drop_table("link_configs")
    op.drop_table("data_sources")
    op.drop_index("ix_template_components_template_id", "template_components")
    op.drop_table("template_components")
    op.drop_table("templates")
