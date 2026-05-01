"""
SQLAlchemy ORM models for the template database.
JSON columns store complex nested structures (pipeline configs, canvas layouts).
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _new_id() -> str:
    return str(uuid.uuid4())


class Base(DeclarativeBase):
    pass


class TemplateModel(Base):
    __tablename__ = "templates"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_id)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    output_format: Mapped[str] = mapped_column(String(10), nullable=False)  # docx | xlsx
    excel_config: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow, onupdate=_utcnow)

    components: Mapped[list["ComponentModel"]] = relationship(
        back_populates="template", cascade="all, delete-orphan", lazy="selectin"
    )


class ComponentModel(Base):
    __tablename__ = "template_components"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_id)
    template_id: Mapped[str] = mapped_column(ForeignKey("templates.id", ondelete="CASCADE"))
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    position: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    content: Mapped[str] = mapped_column(Text, default="")
    source_table: Mapped[str] = mapped_column(String(255), default="")
    source_field: Mapped[str] = mapped_column(String(255), default="")
    columns: Mapped[list] = mapped_column(JSONB, default=list)
    repeat_over: Mapped[str] = mapped_column(String(255), default="")
    transformations: Mapped[list] = mapped_column(JSONB, default=list)
    sort_order: Mapped[int] = mapped_column(default=0)

    template: Mapped[TemplateModel] = relationship(back_populates="components")


class DataSourceModel(Base):
    __tablename__ = "data_sources"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_id)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    db_type: Mapped[str] = mapped_column(String(20), nullable=False)  # postgres | mysql | mongodb
    db_url: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)


class LinkConfigModel(Base):
    __tablename__ = "link_configs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_id)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    tables: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
