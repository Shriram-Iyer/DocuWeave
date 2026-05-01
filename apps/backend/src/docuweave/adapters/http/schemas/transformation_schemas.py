from typing import Any
from pydantic import BaseModel


class ValidatePipelineRequest(BaseModel):
    field_type: str  # string | number | boolean | date | array | object
    pipeline: list[dict[str, Any]]


class ValidatePipelineResponse(BaseModel):
    is_valid: bool
    errors: list[str]


class PreviewPipelineRequest(BaseModel):
    field_type: str
    pipeline: list[dict[str, Any]]
    sample_data: dict[str, Any]  # a single row dict


class PreviewPipelineResponse(BaseModel):
    result: Any
    errors: list[str]
