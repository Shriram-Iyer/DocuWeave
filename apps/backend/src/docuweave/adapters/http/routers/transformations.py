from fastapi import APIRouter

from docuweave.adapters.http.schemas.transformation_schemas import (
    PreviewPipelineRequest,
    PreviewPipelineResponse,
    ValidatePipelineRequest,
    ValidatePipelineResponse,
)
from docuweave.domain.value_objects.field_type import FieldType
from docuweave.use_cases.transformations.validate_pipeline import validate_pipeline
from docuweave.use_cases.transformations.execute_pipeline import execute_pipeline

router = APIRouter(prefix="/api/v1/transformations", tags=["transformations"])


@router.post("/validate", response_model=ValidatePipelineResponse)
async def validate(body: ValidatePipelineRequest) -> ValidatePipelineResponse:
    try:
        field_type = FieldType(body.field_type)
    except ValueError:
        return ValidatePipelineResponse(is_valid=False, errors=[f"Unknown field_type: '{body.field_type}'"])

    is_valid, errors = validate_pipeline(field_type, body.pipeline)
    return ValidatePipelineResponse(is_valid=is_valid, errors=errors)


@router.post("/preview", response_model=PreviewPipelineResponse)
async def preview(body: PreviewPipelineRequest) -> PreviewPipelineResponse:
    try:
        field_type = FieldType(body.field_type)
    except ValueError:
        return PreviewPipelineResponse(result=None, errors=[f"Unknown field_type: '{body.field_type}'"])

    is_valid, errors = validate_pipeline(field_type, body.pipeline)
    if not is_valid:
        return PreviewPipelineResponse(result=None, errors=errors)

    try:
        result = execute_pipeline(body.sample_data, body.pipeline, dataset=[body.sample_data])
        return PreviewPipelineResponse(result=result, errors=[])
    except Exception as e:
        return PreviewPipelineResponse(result=None, errors=[str(e)])
