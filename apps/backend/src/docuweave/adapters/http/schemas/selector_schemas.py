from typing import Any
from pydantic import BaseModel


class SelectorConfigSchema(BaseModel):
    type: str = "table_selector"
    table: str
    display_fields: list[str]
    multi_select: bool = True


class SelectorOptionsRequest(BaseModel):
    data_source_id: str
    selector_config: SelectorConfigSchema


class SelectorEvaluateRequest(BaseModel):
    data_source_id: str
    selector_config: SelectorConfigSchema
    selected_ids: list[str]
