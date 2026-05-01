"""
Beanie Document models for MongoDB template DB.
Mirror the same entities as the SQLAlchemy models.
"""
from datetime import datetime, timezone
from typing import Any

from beanie import Document
from pydantic import Field


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class TemplateDocument(Document):
    name: str
    output_format: str  # docx | xlsx
    excel_config: dict[str, Any] | None = None
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "templates"


class ComponentDocument(Document):
    template_id: str
    type: str
    position: dict[str, Any] = Field(default_factory=dict)
    content: str = ""
    source_table: str = ""
    source_field: str = ""
    columns: list[dict[str, str]] = Field(default_factory=list)
    repeat_over: str = ""
    transformations: list[dict[str, Any]] = Field(default_factory=list)
    sort_order: int = 0

    class Settings:
        name = "template_components"


class DataSourceDocument(Document):
    name: str
    db_type: str
    db_url: str
    created_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "data_sources"


class LinkConfigDocument(Document):
    name: str
    tables: list[dict[str, Any]] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=_utcnow)

    class Settings:
        name = "link_configs"
