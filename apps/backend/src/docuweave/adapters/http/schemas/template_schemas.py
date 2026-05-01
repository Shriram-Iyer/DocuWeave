from typing import Any
from pydantic import BaseModel, Field
import uuid


def _new_id() -> str:
    return str(uuid.uuid4())


class CanvasPositionSchema(BaseModel):
    x: float = 0
    y: float = 0
    width: float = 300
    height: float | str = "auto"


class ComponentCreateRequest(BaseModel):
    type: str  # text | table | image | dynamic_field | repeat_block
    position: CanvasPositionSchema = Field(default_factory=CanvasPositionSchema)
    content: str = ""
    source_table: str = ""
    source_field: str = ""
    columns: list[dict[str, str]] = Field(default_factory=list)
    repeat_over: str = ""
    transformations: list[dict[str, Any]] = Field(default_factory=list)
    sort_order: int = 0


class ComponentResponse(ComponentCreateRequest):
    id: str
    template_id: str


class TemplateCreateRequest(BaseModel):
    name: str
    output_format: str = "docx"  # docx | xlsx
    excel_config: dict[str, Any] | None = None


class TemplateUpdateRequest(BaseModel):
    name: str | None = None
    output_format: str | None = None
    excel_config: dict[str, Any] | None = None


class TemplateResponse(BaseModel):
    id: str
    name: str
    output_format: str
    excel_config: dict[str, Any] | None = None
    components: list[ComponentResponse] = Field(default_factory=list)
