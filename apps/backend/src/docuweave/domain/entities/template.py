from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class TemplateComponent:
    id: str
    type: str  # text | table | image | dynamic_field | repeat_block
    position: dict[str, Any]  # {x, y, width, height}
    content: str = ""
    source_table: str = ""
    source_field: str = ""
    columns: tuple[dict[str, str], ...] = field(default_factory=tuple)
    repeat_over: str = ""
    transformations: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    sub_components: tuple["TemplateComponent", ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class Template:
    id: str
    name: str
    output_format: str  # docx | xlsx
    components: tuple[TemplateComponent, ...] = field(default_factory=tuple)
    # For Excel mode: stores Fortune Sheet workbook JSON config
    excel_config: dict[str, Any] | None = None
